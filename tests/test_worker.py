import asyncio
import os
import json

from dotenv import load_dotenv

from shared.database import MongoConnector
from shared.environment import DEFAULT_DB_NAME, ENV_PATH, PROJECT_ROOT_PATH
from shared.dynamic_env import create_dynamic_environment
from shared.log_config import setup_logging
from worker.job import JobDispatcher


load_dotenv(ENV_PATH)

MONGO_URI = os.getenv('MONGO_URI')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
BUCKET_NAME = os.getenv('BUCKET_NAME')
DB_NAME = os.getenv('DB_NAME')
TEST_REQUEST_PATH = os.path.join(PROJECT_ROOT_PATH, 'tests', 'test_fixtures', 'test_request_without_smoldyn.json')

logger = setup_logging(__file__)
db_connector = MongoConnector(connection_uri=MONGO_URI, database_id=DEFAULT_DB_NAME, local=True)
dispatcher = JobDispatcher(db_connector=db_connector)


async def test_dispatcher():
    with open(TEST_REQUEST_PATH, 'r') as json_file:
        test_request = json.load(json_file)

    print(test_request)
    await dispatcher.dispatch(test_request)

    # get job change confirmation:
    result = await dispatcher.db_connector.read(collection_name="compose_jobs", job_id=test_request['job_id'])


if __name__ == '__main__':
    asyncio.run(test_dispatcher())


