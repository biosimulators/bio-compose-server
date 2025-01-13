""""
Alex Patrie 1/6/2025

NOTE: This workflow is run by the microservices architecture and offloads ALL simulation logic to Biosimulator Processes!

The general workflow should be:

1. gateway: client uploads JSON spec file
2. gateway: gateway stores the JSON spec as a job in mongo
3. gateway: spec is returned to client as confirmation
4. worker: check for pending statuses in mongo collection (single)
5. worker: get simulators/deps from #4 TODO: somehow do this!!
6. worker: dynamic install #5
7. worker: change job status in DB to IN_PROGRESS
8. worker: run composition with pbg.Composite() and gather_results()
9. worker: change job status in DB to COMPLETE
10. worker: update job document ['results'] field with #8's data
11. worker: perhaps emit an event?
"""
import asyncio
import json
import subprocess
import tempfile

import dotenv
import os
from typing import Any, Mapping, List

from process_bigraph import Composite

from shared.database import MongoConnector
from shared.dynamic_env import install_request_dependencies
from shared.log_config import setup_logging
from shared.environment import DEFAULT_LOCAL_MONGO_URI, DEFAULT_DB_NAME, DEFAULT_DB_TYPE, DEFAULT_JOB_COLLECTION_NAME

logger = setup_logging(__file__)


class JobDispatcher(object):
    def __init__(self,
                 db_connector: MongoConnector,
                 timeout: int = 5):
        """
        :param db_connector: (`shared.database.MongoConnector`) database connector singleton instantiated with mongo uri.
        :param timeout: number of minutes for timeout. Default is 5 minutes
        """
        self.db_connector = db_connector
        self.timeout = timeout * 60

    @property
    def current_jobs(self) -> List[Mapping[str, Any]]:
        return self.db_connector.get_jobs()

    async def run(self):
        # iterate over all jobs
        print('checking jobs...')
        i = 0
        while i < 5:
            for job in self.current_jobs:
                await self.dispatch(job)
            i += 1
            print('sleeping')
            await asyncio.sleep(1)

    @staticmethod
    def generate_failed_job(job_id: str, msg: str):
        return {"job_id": job_id, "status": "FAILED", "result": msg}

    async def install_simulators(self, job: Mapping[str, Any]):
        simulators = job["simulators"]
        return install_request_dependencies(simulators)

    async def dispatch(self, job: Mapping[str, Any]):
        # TODO: add try blocks for each section
        job_status = job["status"]
        if job_status.lower() != "pending":
            # job_id = job["job_id"]
            # print(f'Dispatching job {job_id}...')
            # simulators = job["simulators"]
            # try:
            #     installation_resp = install_request_dependencies(simulators)
            # except subprocess.CalledProcessError as e:
            #     msg = f"Attempted installation for Job {job_id} was not successful."
            #     logger.error(msg)
            #     return {"job_id": job_id, "status": "FAILED", "result": msg}

            # 3. install simulators required
            await self.install_simulators(job)

            # 4. change job status to IN_PROGRESS
            job_id = job["job_id"]
            await self.db_connector.update_job(job_id=job_id, status="IN_PROGRESS")

            # 5. from bsp import app_registrar.core
            bsp = __import__("bsp")
            core = bsp.app_registrar.core

            # 6. create Composite() with core and job["job_spec"]
            composition = Composite(
                config={"state": job["spec"]},
                core=core
            )

            # 7. run composition with instance from #6 for specified duration (default 1)
            dur = job.get("duration", 1)
            composition.run(dur)

            # 8. get composition results indexed from ram-emitter
            results = composition.gather_results()[("emitter",)]

            # 9. update job in DB ['results'] to Composite().gather_results() AND change status to COMPLETE
            await self.db_connector.update_job(job_id=job_id, status="COMPLETE", results=results)

            # 10. add new result state in db within result_states collection!
            temp_dir = tempfile.mkdtemp()
            temp_fname = f"{job}.state.json"
            composition.save(filename=temp_fname, outdir=temp_dir)
            temp_path = os.path.join(temp_dir, temp_fname)
            with open(temp_path, 'r') as f:
                current_data = json.load(f)
            await self.db_connector.write(
                collection_name="result_states",
                job_id=job_id,
                data=current_data,
                last_updated=self.db_connector.timestamp()
            )

            # 11. remove composite state file artifact
            os.remove(temp_path) if os.path.exists(temp_path) else None


def test_dispatcher():
    from shared.data_model import CompositionRun
    import asyncio

    dispatcher = JobDispatcher(connection_uri=DEFAULT_LOCAL_MONGO_URI, database_id=DEFAULT_DB_NAME)
    jid = "test"

    test_run = CompositionRun(
        job_id=jid,
        last_updated="n/a",
        simulators=['copasi'],
        duration=1,
        spec={'a': {}},
        status="PENDING",
        results={}
    )

    confirmation = asyncio.run(
        dispatcher.db_connector.write(collection_name=DEFAULT_JOB_COLLECTION_NAME, **test_run.to_dict())
    )

    print(f'STORED: {confirmation}')

    asyncio.run(
        dispatcher.run()
    )




