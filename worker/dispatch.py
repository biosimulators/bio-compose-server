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
from shared.dynamic_env import install_request_dependencies, create_dynamic_environment
from shared.log_config import setup_logging
from shared.environment import DEFAULT_DB_NAME, DEFAULT_DB_TYPE, DEFAULT_JOB_COLLECTION_NAME, PROJECT_ROOT_PATH
from worker.workers.runs import RunsWorker
from worker.workers.composition import CompositionWorker

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
        i = 0
        while i < 5:
            for job in self.current_jobs:
                job_id = job['job_id']
                if job_id.startswith("run"):
                    await RunsWorker().dispatch(job=job, db_connector=self.db_connector)
                else:
                    await CompositionWorker().dispatch(job=job, db_connector=self.db_connector)
            i += 1
            await asyncio.sleep(1)

    @staticmethod
    def generate_failed_job(job_id: str, msg: str):
        return {"job_id": job_id, "status": "FAILED", "result": msg}


def test_dispatcher():
    from shared.data_model import CompositionRun
    import asyncio




