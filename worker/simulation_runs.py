import tempfile
from typing import Dict

from shared.environment import DEFAULT_BUCKET_NAME
from shared.io import download_file, format_smoldyn_configuration


class SimulationRunner(object):
    async def run(self, job: Dict):
        source_fp = job.get('path')
        # case: is either utc or smoldyn
        if source_fp is not None:
            out_dir = tempfile.mkdtemp()
            local_fp = download_file(source_blob_path=source_fp, out_dir=out_dir, bucket_name=DEFAULT_BUCKET_NAME)
            if local_fp.endswith('.txt'):
                await self.run_smoldyn(local_fp=local_fp, job=job)
            elif local_fp.endswith('.xml'):
                await self.run_utc(local_fp)
        # case: is readdy (no input file)
        elif "readdy" in job.get('job_id'):
            await self.run_readdy()
        return self.job_result

    async def run_smoldyn(self, local_fp: str, job: Dict):
        # format model file for disabling graphics
        format_smoldyn_configuration(filename=local_fp)

        # get job params
        duration = job.get('duration')
        dt = job.get('dt')
        initial_species_state = job.get('initial_molecule_state')  # not yet implemented

        # execute simularium, pointing to a filepath that is returned by the run smoldyn call
        result = run_smoldyn(model_fp=local_fp, duration=duration, dt=dt)

        # TODO: Instead use the composition framework to do this

        # write the aforementioned output file (which is itself locally written to the temp out_dir, to the bucket if applicable
        results_file = result.get('results_file')
        if results_file is not None:
            uploaded_file_location = await write_uploaded_file(job_id=self.job_id, uploaded_file=results_file, bucket_name=BUCKET_NAME, extension='.txt')
            self.job_result = {'results_file': uploaded_file_location}
        else:
            self.job_result = result

    async def run_readdy(self):
        # get request params
        duration = self.job_params.get('duration')
        dt = self.job_params.get('dt')
        box_size = self.job_params.get('box_size')
        species_config = self.job_params.get('species_config')
        particles_config = self.job_params.get('particles_config')
        reactions_config = self.job_params.get('reactions_config')
        unit_system_config = self.job_params.get('unit_system_config')

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
            uploaded_file_location = await write_uploaded_file(job_id=self.job_id, uploaded_file=results_file, bucket_name=BUCKET_NAME, extension='.h5')
            self.job_result = {'results_file': uploaded_file_location}
            os.remove(results_file)
        else:
            self.job_result = result

    async def run_utc(self, local_fp: str):
        start = self.job_params['start']
        end = self.job_params['end']
        steps = self.job_params['steps']
        simulator = self.job_params.get('simulators')[0]

        result = generate_sbml_outputs(sbml_fp=local_fp, start=start, dur=end, steps=steps, simulators=[simulator])
        self.job_result = result[simulator]