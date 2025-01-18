"""
Server gateway implementation.

Author: Alexander Patrie <@AlexPatrie>
"""

import json
import os
import uuid
from tempfile import mkdtemp

import dotenv
from typing import *
# from tempfile import mkdtemp

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, Query, APIRouter, Body
# from fastapi.responses import FileResponse
from pydantic import BeforeValidator
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from gateway.handlers.submit import submit_utc_run, check_composition

from gateway.handlers.health import check_client
from shared.data_model import (
    BigraphRegistryAddresses,
    CompositionNode,
    CompositionSpec,
    CompositionRun,
    OutputData,
    ValidatedComposition,
    SmoldynRun,
    SimulariumAgentParameters,
    ReaddySpeciesConfig,
    ReaddyReactionConfig,
    ReaddyParticleConfig,
    ReaddyRun,
    AmiciRun,
    CobraRun,
    CopasiRun,
    TelluriumRun,
    IncompleteFileJob,
    APP_SERVERS,
    HealthCheckResponse
)
from shared.database import MongoConnector
from shared.io import write_uploaded_file, download_file_from_bucket
from shared.log_config import setup_logging
from shared.utils import get_project_version, new_job_id
from shared.environment import (
    ENV_PATH,
    DEFAULT_DB_NAME,
    DEFAULT_DB_TYPE,
    DEFAULT_JOB_COLLECTION_NAME,
    DEFAULT_BUCKET_NAME
)


logger = setup_logging(__file__)

# load dev env (local)...see note below
dotenv.load_dotenv(ENV_PATH)  # NOTE: create an env config at this filepath if dev

APP_VERSION = get_project_version()
MONGO_URI = os.getenv("MONGO_URI")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
APP_TITLE = "bio-compose-server"
APP_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://127.0.0.1:4200',
    'http://127.0.0.1:4201',
    'http://127.0.0.1:4202',
    'http://localhost:4200',
    'http://localhost:4201',
    'http://localhost:4202',
    'http://localhost:8000',
    'http://localhost:3001',
    'https://biosimulators.org',
    'https://www.biosimulators.org',
    'https://biosimulators.dev',
    'https://www.biosimulators.dev',
    'https://run.biosimulations.dev',
    'https://run.biosimulations.org',
    'https://biosimulations.dev',
    'https://biosimulations.org',
    'https://bio.libretexts.org',
    'https://compose.biosimulations.org'
]

# -- app components -- #

db_conn_gateway = MongoConnector(connection_uri=MONGO_URI, database_id=DEFAULT_DB_NAME)
router = APIRouter()
app = FastAPI(title=APP_TITLE, version=APP_VERSION, servers=APP_SERVERS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=APP_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mongo_client = db_conn_gateway.client

# It will be represented as a `str` on the model so that it can be serialized to JSON. Represents an ObjectId field in the database.
PyObjectId = Annotated[str, BeforeValidator(str)]


# -- Composition: submit composition jobs --

@app.get(
    "/get-process-bigraph-addresses",
    operation_id="get-process-bigraph-addresses",
    response_model=BigraphRegistryAddresses,
    tags=["Composition"],
    summary="Get process bigraph implementation addresses for composition specifications.")
async def get_process_bigraph_addresses() -> BigraphRegistryAddresses:
    # TODO: adjust this. Currently, if the optional simulator dep is not included, the process implementations will not show up
    from bsp import app_registrar
    addresses = app_registrar.registered_addresses
    version = "latest"

    return BigraphRegistryAddresses(registered_addresses=addresses, version=version)
    # else:
    #     raise HTTPException(status_code=500, detail="Addresses not found.")


@app.post(
    "/validate-composition",
    response_model=ValidatedComposition,
    tags=["Composition"],
    operation_id="validate-composition",
    summary="Validate Simulation Experiment Design specification file.",
)
async def validate_composition(
        spec_file: UploadFile = File(..., description="Composition JSON File"),
) -> ValidatedComposition:
    # validate filetype
    if not spec_file.filename.endswith('.json') and spec_file.content_type != 'application/json':
        raise HTTPException(status_code=400, detail="Invalid file type. Only JSON files are supported.")

    # multifold IO verification:
    try:
        contents = await spec_file.read()
        document_data: Dict = json.loads(contents)
        return check_composition(document_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format.")


@app.post(
    "/submit-composition",
    response_model=CompositionRun,
    tags=["Composition"],
    operation_id="submit-composition",
    summary="Submit composition spec for simulation",
)
async def submit_composition(
        spec_file: UploadFile = File(..., description="Composition JSON File"),
        # simulators: List[str] = Query(..., description="Simulator package names to use for implementation"),
        duration: int = Query(..., description="Duration of simulation"),
        model_files: List[UploadFile] = File(...),
) -> CompositionRun:
    # validate filetype
    if not spec_file.filename.endswith('.json') and spec_file.content_type != 'application/json':
        raise HTTPException(status_code=400, detail="Invalid file type. Only JSON files are supported.")

    job_id = new_job_id("composition")
    try:
        # 1. verification by fitting a common datamodel (in this case composition spec)
        contents = await spec_file.read()
        data: Dict = json.loads(contents)

        simulators: List[str] = []
        for node_name, node_spec in data.items():
            # parse list of simulators required from spec addresses

            address = node_spec['address']  # MUST be like: local:copasi-process
            if "emitter" not in address:
                simulator = address.split(":")[-1].split('-')[0]
                simulators.append(simulator)

            # upload model files as needed (model filepath MUST match that which is in the spec-->./model-file
            for model_file in model_files:
                spec_model_source = node_spec.get("config").get("model", {}).get("model_source")
                if (spec_model_source == model_file.filename):
                    file_ext = os.path.splitext(spec_model_source)[-1]
                    uploaded_model_source_location = await write_uploaded_file(
                        job_id=job_id,
                        uploaded_file=model_file,
                        bucket_name=DEFAULT_BUCKET_NAME,
                        extension=file_ext
                    )
                    data[node_name]["config"]["model"]["model_source"] = uploaded_model_source_location

        # 1a. verification by fitting the individual process specs to an expected structure
        nodes: List[CompositionNode] = []
        for node_name, node_spec in data.items():
            node = CompositionNode(name=node_name, **node_spec)
            nodes.append(node)

        # 1b. verification by fitting that tree of nodes into an expected structure (which is consumed by pbg.Composite())
        composition = CompositionSpec(
            nodes=nodes,
            emitter_mode="all",
            job_id=job_id
        )

        # 2. verification by fitting write confirmation into CompositionRun...to verify O phase of IO, garbage in garbage out
        write_confirmation: Dict = await db_conn_gateway.write(
            collection_name=DEFAULT_JOB_COLLECTION_NAME,
            status="PENDING",
            spec=composition.spec,
            job_id=composition.job_id,
            last_updated=db_conn_gateway.timestamp(),
            simulators=simulators,
            duration=duration,
            results={}
        )

        return CompositionRun(**write_confirmation)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/get-composition-state/{job_id}",
    operation_id="get-composition-state",
    tags=["Composition"],
    summary="Get the composite spec of a given simulation run indexed by job_id.")
async def get_composition_state(job_id: str):
    try:
        spec = await db_conn_gateway.read(collection_name="result_states", job_id=job_id)
        if "_id" in spec.keys():
            spec.pop("_id")

        return spec
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=f"No specification found for job with id: {job_id}.")


# -- Data: output data --

@app.get(
    "/get-output/{job_id}",
    response_model=OutputData,
    operation_id='get-output',
    tags=["Data"],
    summary='Get the results of an existing simulation run.')
async def get_output(job_id: str):
    # get the job
    job = await db_conn_gateway.read(collection_name=DEFAULT_JOB_COLLECTION_NAME, job_id=job_id)

    # parse id and return if job exist
    if job is not None:
        not_included = ["_id", "spec", "duration", "simulators"]
        data = {}
        for key in job.keys():
            if key not in not_included:
                data[key] = job[key]

        return OutputData(**data)
    else:
        # otherwise, job does not exists
        msg = f"Job with id: {job_id} not found. Please check the job_id and try again."
        logger.error(msg)
        raise HTTPException(status_code=404, detail=msg)


@app.get(
    "/get-output-file/{job_id}",
    operation_id='get-output-file',
    tags=["Data"],
    summary='Get the results of an existing simulation run from Smoldyn or Readdy as either a downloadable file or job progression status.'
)
async def get_output_file(job_id: str):
    # state-case: job is completed
    if not job_id.startswith("simulation-execution"):
        raise HTTPException(status_code=404, detail="This must be an output file job query starting with 'simulation-execution'.")
    job = await db_conn_gateway.read(collection_name="completed_jobs", job_id=job_id)
    if job is not None:
        # rm mongo index
        job.pop('_id', None)
        # parse filepath in bucket and create file response
        job_data = job
        if isinstance(job_data, dict):
            remote_fp = job_data.get("results").get("results_file")
            if remote_fp is not None:
                temp_dest = mkdtemp()
                local_fp = download_file_from_bucket(source_blob_path=remote_fp, out_dir=temp_dest, bucket_name=DEFAULT_BUCKET_NAME)
                # return downloadable file blob
                return FileResponse(path=local_fp, media_type="application/octet-stream", filename=local_fp.split("/")[-1])  # TODO: return special smoldyn file instance
    # state-case: job has failed
    if job is None:
        job = await db_conn_gateway.read(collection_name="failed_jobs", job_id=job_id)
    # state-case: job is not in completed:
    if job is None:
        job = await db_conn_gateway.read(collection_name="in_progress_jobs", job_id=job_id)
    # state-case: job is not in progress:
    if job is None:
        job = await db_conn_gateway.read(collection_name="pending_jobs", job_id=job_id)
    # case: job is either failed, in prog, or pending
    if job is not None:
        # rm mongo index
        job.pop('_id', None)
        # specify source safely
        src = job.get('source', job.get('path'))
        if src is not None:
            source = src.split('/')[-1]
        else:
            source = None

        return IncompleteFileJob(
            job_id=job_id,
            timestamp=job.get('timestamp'),
            status=job.get('status'),
            source=source
        )


# -- Files: submit file IO jobs --

@app.post(
    "/generate-simularium-file",
    operation_id='generate-simularium-file',
    tags=["Files"],
    summary='Generate a simularium file with a compatible simulation results file from Smoldyn')
async def generate_simularium_file(
        uploaded_file: UploadFile = File(..., description="A file containing results that can be parse by Simularium (spatial)."),
        box_size: float = Query(..., description="Size of the simulation box as a floating point number."),
        filename: str = Query(default=None, description="Name desired for the simularium file. NOTE: pass only the file name without an extension."),
        translate_output: bool = Query(default=True, description="Whether to translate the output trajectory prior to converting to simularium. See simulariumio documentation for more details."),
        validate_output: bool = Query(default=True, description="Whether to validate the outputs for the simularium file. See simulariumio documentation for more details."),
        agent_parameters: SimulariumAgentParameters = Body(default=None, description="Parameters for the simularium agents defining either radius or mass and density.")
):
    job_id = "files-generate-simularium-file" + str(uuid.uuid4())
    _time = db_conn_gateway.timestamp()
    uploaded_file_location = await write_uploaded_file(
        job_id=job_id,
        uploaded_file=uploaded_file,
        bucket_name=DEFAULT_BUCKET_NAME,
        extension='.txt'
    )

    # new simularium job in db
    if filename is None:
        filename = 'simulation'
    agent_params = {}
    if agent_parameters is not None:
        for agent_param in agent_parameters.agents:
            agent_params[agent_param.name] = agent_param.serialize()

    new_job_submission = await db_conn_gateway.write(
        collection_name=DEFAULT_JOB_COLLECTION_NAME,
        status="PENDING",
        job_id=job_id,
        timestamp=_time,
        path=uploaded_file_location,
        filename=filename,
        box_size=box_size,
        translate_output=translate_output,
        validate_output=validate_output,
        agent_parameters=agent_params if agent_params is not {} else None
    )
    gen_id = new_job_submission.get('_id')
    if gen_id is not None:
        new_job_submission.pop('_id')

    return new_job_submission


# -- Health: check health status --

@app.get(
    "/",
    tags=["Health"],
    summary="Health check",
    response_model=HealthCheckResponse,
)
def check_health() -> HealthCheckResponse:
    response = check_client(db_conn_gateway)
    return HealthCheckResponse(
        version=APP_VERSION,
        status="running" if response.status == "PASS" else response
    )


# -- Processes: submit single simulator jobs --

@app.post(
    "/run-amici-process",
    response_model=AmiciRun,
    name="Run an Amici simulation",
    operation_id="run-amici-process",
    tags=["Processes"],
    summary="Run a Amici simulation.")
async def run_amici_process(
    model_file: UploadFile = File(..., description="SBML file"),
    start: int = Query(..., description="Start time"),
    stop: int = Query(..., description="End time(duration)"),
    steps: int = Query(..., description="Number of steps.")
) -> AmiciRun:
    run_data = await submit_utc_run(
        db_connector=db_conn_gateway,
        simulator="amici",
        model_file=model_file,
        implementation_scope="process",
        start=start,
        stop=stop,
        steps=steps,
        context_model=AmiciRun,
        logger=logger
    )

    return run_data


@app.post(
    "/run-cobra-process",
    response_model=CobraRun,
    name="Run an cobra simulation",
    operation_id="run-cobra-process",
    tags=["Processes"],
    summary="Run a cobra simulation.")
async def run_cobra_process(
    model_file: UploadFile = File(..., description="SBML file"),
    start: int = Query(..., description="Start time"),
    stop: int = Query(..., description="End time(duration)"),
    steps: int = Query(..., description="Number of steps.")
) -> CobraRun:
    run_data = await submit_utc_run(
        db_connector=db_conn_gateway,
        simulator="cobra",
        model_file=model_file,
        implementation_scope="process",
        start=start,
        stop=stop,
        steps=steps,
        context_model=CobraRun,
        logger=logger
    )

    return run_data


@app.post(
    "/run-copasi-process",
    response_model=CopasiRun,
    name="Run an copasi simulation",
    operation_id="run-copasi-process",
    tags=["Processes"],
    summary="Run a copasi simulation.")
async def run_copasi_process(
    model_file: UploadFile = File(..., description="SBML file"),
    start: int = Query(..., description="Start time"),
    stop: int = Query(..., description="End time(duration)"),
    steps: int = Query(..., description="Number of steps.")
) -> CopasiRun:
    run_data = await submit_utc_run(
        db_connector=db_conn_gateway,
        simulator="copasi",
        model_file=model_file,
        implementation_scope="process",
        start=start,
        stop=stop,
        steps=steps,
        context_model=CopasiRun,
        logger=logger
    )

    return run_data


@app.post(
    "/run-tellurium-process",
    response_model=TelluriumRun,
    name="Run an tellurium simulation",
    operation_id="run-tellurium-process",
    tags=["Processes"],
    summary="Run a tellurium simulation.")
async def run_tellurium_process(
    model_file: UploadFile = File(..., description="SBML file"),
    start: int = Query(..., description="Start time"),
    stop: int = Query(..., description="End time(duration)"),
    steps: int = Query(..., description="Number of steps.")
) -> TelluriumRun:
    run_data = await submit_utc_run(
        db_connector=db_conn_gateway,
        simulator="tellurium",
        model_file=model_file,
        implementation_scope="process",
        start=start,
        stop=stop,
        steps=steps,
        context_model=TelluriumRun,
        logger=logger
    )

    return run_data


# -- Steps: submit single simulator jobs --

@app.post(
    "/run-amici-step",
    response_model=AmiciRun,
    name="Run an Amici simulation",
    operation_id="run-amici-step",
    tags=["Steps"],
    summary="Run a Amici simulation.")
async def run_amici_step(
    model_file: UploadFile = File(..., description="SBML file"),
    start: int = Query(..., description="Start time"),
    stop: int = Query(..., description="End time(duration)"),
    steps: int = Query(..., description="Number of steps.")
) -> AmiciRun:
    run_data = await submit_utc_run(
        db_connector=db_conn_gateway,
        simulator="amici",
        model_file=model_file,
        implementation_scope="step",
        start=start,
        stop=stop,
        steps=steps,
        context_model=AmiciRun,
        logger=logger
    )

    return run_data


@app.post(
    "/run-cobra-step",
    response_model=CobraRun,
    name="Run an cobra simulation",
    operation_id="run-cobra-step",
    tags=["Steps"],
    summary="Run a cobra simulation.")
async def run_cobra_step(
    model_file: UploadFile = File(..., description="SBML file"),
    start: int = Query(..., description="Start time"),
    stop: int = Query(..., description="End time(duration)"),
    steps: int = Query(..., description="Number of steps.")
) -> CobraRun:
    run_data = await submit_utc_run(
        db_connector=db_conn_gateway,
        simulator="cobra",
        model_file=model_file,
        implementation_scope="step",
        start=start,
        stop=stop,
        steps=steps,
        context_model=CobraRun,
        logger=logger
    )

    return run_data


@app.post(
    "/run-copasi-step",
    response_model=CopasiRun,
    name="Run an copasi simulation",
    operation_id="run-copasi-step",
    tags=["Steps"],
    summary="Run a copasi simulation.")
async def run_copasi_step(
    model_file: UploadFile = File(..., description="SBML file"),
    start: int = Query(..., description="Start time"),
    stop: int = Query(..., description="End time(duration)"),
    steps: int = Query(..., description="Number of steps.")
) -> CopasiRun:
    run_data = await submit_utc_run(
        db_connector=db_conn_gateway,
        simulator="copasi",
        model_file=model_file,
        implementation_scope="step",
        start=start,
        stop=stop,
        steps=steps,
        context_model=CopasiRun,
        logger=logger
    )

    return run_data


@app.post(
    "/run-readdy-step",
    response_model=ReaddyRun,
    name="Run a readdy simulation",
    operation_id="run-readdy-step",
    tags=["Steps"],
    summary="Run a readdy simulation.")
async def run_readdy_step(
        box_size: List[float] = Query(default=[0.3, 0.3, 0.3], description="Box Size of box"),
        duration: int = Query(default=10, description="Simulation Duration"),
        dt: float = Query(default=0.0008, description="Interval of step with which simulation runs"),
        species_config: List[ReaddySpeciesConfig] = Body(
            ...,
            description="Species Configuration, specifying species name mapped to diffusion constant",
            examples=[
                [
                    {"name": "E",  "diffusion_constant": 10.0},
                    {"name": "S",  "diffusion_constant": 10.0},
                    {"name": "ES", "diffusion_constant": 10.0},
                    {"name": "P", "diffusion_constant": 10.0}
                ]
            ]
        ),
        reactions_config: List[ReaddyReactionConfig] = Body(
            ...,
            description="Reactions Configuration, specifying reaction scheme mapped to reaction constant.",
            examples=[
                [
                    {"scheme": "fwd: E +(0.03) S -> ES", "rate": 86.78638438},
                    {"scheme": "back: ES -> E +(0.03) S", "rate": 1.0},
                    {"scheme": "prod: ES -> E +(0.03) P", "rate": 1.0},
                ]
            ]
        ),
        particles_config: List[ReaddyParticleConfig] = Body(
            ...,
            description="Particles Configuration, specifying initial particle positions for each particle.",
            examples=[
                [
                    {
                        "name": "E",
                        "initial_positions": [
                            [-0.11010841, 0.01048227, -0.07514985],
                            [0.02715631, -0.03829782, 0.14395517],
                            [0.05522253, -0.11880506, 0.02222362]
                        ]
                    },
                    {
                        "name": "S",
                        "initial_positions": [
                            [-0.21010841, 0.21048227, -0.07514985],
                            [0.02715631, -0.03829782, 0.14395517],
                            [0.05522253, -0.11880506, 0.02222362]
                        ]
                    }
                ]
            ]
        ),
        unit_system_config: Dict[str, str] = Body({"length_unit": "micrometer", "time_unit": "second"}, description="Unit system configuration"),
        reaction_handler: str = Query(default="UncontrolledApproximation", description="Reaction handler as per Readdy simulation documentation.")
) -> ReaddyRun:
    try:
        # get job params
        job_id = "simulation-execution-readdy" + str(uuid.uuid4())
        _time = db_conn_gateway.timestamp()

        # instantiate new return
        readdy_run = ReaddyRun(
            job_id=job_id,
            last_updated=_time,
            box_size=box_size,
            status="PENDING",
            duration=duration,
            dt=dt,
            species_config=species_config,
            reactions_config=reactions_config,
            particles_config=particles_config,
            unit_system_config={"length_unit": "micrometer", "time_unit": "second"},
            reaction_handler="UncontrolledApproximation"
        )

        # insert job
        pending_job = await db_conn_gateway.write(
            collection_name=DEFAULT_JOB_COLLECTION_NAME,
            box_size=readdy_run.box_size,
            job_id=readdy_run.job_id,
            last_updated=readdy_run.last_updated,
            status=readdy_run.status,
            duration=readdy_run.duration,
            dt=readdy_run.dt,
            species_config=[config.serialize() for config in readdy_run.species_config],
            reactions_config=[config.serialize() for config in readdy_run.reactions_config],
            particles_config=[config.serialize() for config in readdy_run.particles_config],
            unit_system_config=readdy_run.unit_system_config,
            reaction_handler=readdy_run.reaction_handler
        )

        return readdy_run
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/run-smoldyn-step",
    response_model=SmoldynRun,
    name="Run a smoldyn simulation",
    operation_id="run-smoldyn-step",
    tags=["Steps"],
    summary="Run a smoldyn simulation.")
async def run_smoldyn_step(
        uploaded_file: UploadFile = File(..., description="Smoldyn Configuration File"),
        duration: int = Query(default=None, description="Simulation Duration"),
        dt: float = Query(default=None, description="Interval of step with which simulation runs"),
        # initial_molecule_state: List = Body(default=None, description="Mapping of species names to initial molecule conditions including counts and location.")
) -> SmoldynRun:
    try:
        # get job params
        job_id = "simulation-execution-smoldyn" + str(uuid.uuid4())
        _time = db_conn_gateway.timestamp()
        uploaded_file_location = await write_uploaded_file(job_id=job_id, uploaded_file=uploaded_file, bucket_name=DEFAULT_BUCKET_NAME, extension='.txt')
        # instantiate new return
        smoldyn_run = SmoldynRun(
            job_id=job_id,
            last_updated=_time,
            status="PENDING",
            path=uploaded_file_location,
            duration=duration,
            dt=dt
        )
        # insert job
        pending_job = await db_conn_gateway.write(
            collection_name="smoldyn_jobs",
            job_id=smoldyn_run.job_id,
            last_updated=smoldyn_run.last_updated,
            status=smoldyn_run.status,
            path=smoldyn_run.path,
            duration=smoldyn_run.duration,
            dt=smoldyn_run.dt
        )

        return smoldyn_run
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/run-tellurium-step",
    response_model=TelluriumRun,
    name="Run an tellurium simulation",
    operation_id="run-tellurium-step",
    tags=["Steps"],
    summary="Run a tellurium simulation.")
async def run_tellurium_step(
    model_file: UploadFile = File(..., description="SBML file"),
    start: int = Query(..., description="Start time"),
    stop: int = Query(..., description="End time(duration)"),
    steps: int = Query(..., description="Number of steps.")
) -> TelluriumRun:
    run_data = await submit_utc_run(
        db_connector=db_conn_gateway,
        simulator="tellurium",
        model_file=model_file,
        implementation_scope="step",
        start=start,
        stop=stop,
        steps=steps,
        context_model=TelluriumRun,
        logger=logger
    )

    return run_data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)

