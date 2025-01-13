import asyncio
import sys
import tempfile
import json
import os

from process_bigraph import Composite

from shared.database import MongoConnector
from shared.environment import DEFAULT_DB_NAME

job = sys.argv[1]
job_id = sys.argv[2]
job = json.loads(job)
mongo_uri = sys.argv[3]
local_connection = sys.argv[4]


async def run():
    db_connector = MongoConnector(connection_uri=mongo_uri, database_id=DEFAULT_DB_NAME, local=bool(int(local_connection)))
    # from bsp import app_registrar.core
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
    await db_connector.update_job(job_id=job_id, status="COMPLETE", results=results)
    # 10. add new result state in db within result_states collection!
    temp_dir = tempfile.mkdtemp()
    temp_fname = f"{job}.state.json"
    composition.save(filename=temp_fname, outdir=temp_dir)
    temp_path = os.path.join(temp_dir, temp_fname)
    with open(temp_path, 'r') as f:
        current_data = json.load(f)
    await db_connector.write(
        collection_name="result_states",
        job_id=job_id,
        data=current_data,
        last_updated=db_connector.timestamp()
    )
    # 11. remove composite state file artifact
    os.remove(temp_path) if os.path.exists(temp_path) else None


if __name__ == "__main__":
    asyncio.run(run())
