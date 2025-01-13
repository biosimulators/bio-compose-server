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
db_connector = MongoConnector(connection_uri=MONGO_URI, database_id=DEFAULT_DB_NAME)
dispatcher = JobDispatcher()# (db_connector=db_connector)


def test_dispatcher():
    with open(TEST_REQUEST_PATH, 'r') as json_file:
        test_request = json.load(json_file)

    print(test_request)
    dispatcher.dispatch(test_request)


def test_dynamic_install():
    with open(TEST_REQUEST_PATH, 'r') as json_file:
        job = json.load(json_file)

    installation_resp = asyncio.run(dispatcher.install_simulators(job))
    print(installation_resp)


def test_dynamic_env():
    with open(TEST_REQUEST_PATH, 'r') as json_file:
        job = json.load(json_file)

    create_dynamic_environment(job)


if __name__ == '__main__':
    test_dispatcher()
    # test_dynamic_install()
    # test_dynamic_env()


