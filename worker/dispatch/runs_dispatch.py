import os
import tempfile
from typing import Dict

from bsp.data_generators import generate_sbml_outputs

from shared.environment import DEFAULT_BUCKET_NAME
from shared.io import download_file, format_smoldyn_configuration, write_uploaded_file
from worker.data_generator import run_smoldyn, run_readdy, generate_sbml_utc_outputs


# TODO: standardize this class as a base class

class RunsDispatcher(object):
    async def run(self, job: Dict):
        result = {}
        source_fp = job.get('path')
        # case: is either utc or smoldyn
        if source_fp is not None:
            out_dir = tempfile.mkdtemp()
            local_fp = download_file(source_blob_path=source_fp, out_dir=out_dir, bucket_name=DEFAULT_BUCKET_NAME)
            if local_fp.endswith('.txt'):
                result = await self.run_smoldyn(local_fp=local_fp, job=job)
            elif local_fp.endswith('.xml'):
                result = await self.run_utc(local_fp=local_fp, job=job)
        # case: is readdy (no input file)
        elif "readdy" in job.get('job_id'):
            result = await self.run_readdy(job)

        return result

    async def run_smoldyn(self, local_fp: str, job: Dict):
        # format model file for disabling graphics
        format_smoldyn_configuration(filename=local_fp)

        # get job params
        duration = job.get('duration')
        dt = job.get('dt')
        initial_species_state = job.get('initial_molecule_state')  # not yet implemented
        job_id = job.get('job_id')

        # execute simularium, pointing to a filepath that is returned by the run smoldyn call
        result = run_smoldyn(model_fp=local_fp, duration=duration, dt=dt)

        # write the aforementioned output file (which is itself locally written to the temp out_dir, to the bucket if applicable
        results_file = result.get('results_file')
        if results_file is not None:
            uploaded_file_location = await write_uploaded_file(
                job_id=self.job_id,
                uploaded_file=results_file,
                bucket_name=DEFAULT_BUCKET_NAME,
                extension='.txt'
            )
            return {'results_file': uploaded_file_location}
        else:
            return result

    async def run_readdy(self, job: Dict):
        # get request params
        duration = job.get('duration')
        dt = job.get('dt')
        box_size = job.get('box_size')
        species_config = job.get('species_config')
        particles_config = job.get('particles_config')
        reactions_config = job.get('reactions_config')
        unit_system_config = job.get('unit_system_config')

        # run simulations
        result = run_readdy(
            box_size=box_size,
            species_config=species_config,
            particles_config=particles_config,
            reactions_config=reactions_config,
            unit_system_config=unit_system_config,
            duration=duration,
            dt=dt
        )

        # extract results file and write to bucket
        results_file = result.get('results_file')
        if results_file is not None:
            uploaded_file_location = await write_uploaded_file(
                job_id=self.job_id,
                uploaded_file=results_file,
                bucket_name=DEFAULT_BUCKET_NAME,
                extension='.h5'
            )
            os.remove(results_file)

            return {'results_file': uploaded_file_location}
        else:
            return result

    async def run_utc(self, local_fp: str, job: Dict):
        start = job['start']
        end = job['end']
        steps = job['steps']
        simulator = job.get('simulators')[0]

        result = generate_sbml_utc_outputs(sbml_fp=local_fp, start=start, dur=end, steps=steps, simulators=[simulator])
        return result[simulator]
