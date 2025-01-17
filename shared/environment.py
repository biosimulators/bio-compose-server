"""
Environmental constraints: dynamic and default
"""
import dataclasses
import os

from dotenv import load_dotenv

from shared.data_model import BaseClass

PROJECT_ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

DEFAULT_ENV_PATH = 'shared/.env'
ENV_PATH = os.path.join(PROJECT_ROOT_PATH, DEFAULT_ENV_PATH)
load_dotenv(ENV_PATH)


DEFAULT_DB_TYPE = os.getenv("DB_TYPE", "mongodb")
DEFAULT_DB_NAME = os.getenv("DB_NAME", "compose_db")
DEFAULT_BUCKET_NAME = os.getenv("BUCKET_NAME", "compose_bucket")
DEFAULT_JOB_COLLECTION_NAME = os.getenv("JOB_COLLECTION_NAME", "compose_jobs")
