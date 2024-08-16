import logging
import os
import uuid
from abc import abstractmethod, ABC
from asyncio import sleep
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import *

from dotenv import load_dotenv
from google.cloud import storage
from process_bigraph import ProcessTypes
from pydantic import BaseModel as _BaseModel, ConfigDict
from fastapi import UploadFile
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


# -- globally-shared content-- #

load_dotenv('../assets/.env_dev')

DB_TYPE = "mongo"  # ie: postgres, etc
DB_NAME = "service_requests"
BUCKET_NAME = os.getenv("BUCKET_NAME")
CORE = ProcessTypes()


def unique_id():
    return str(uuid.uuid4())


async def load_arrows(timer):
    check_timer = timer
    ell = ""
    bars = ""
    msg = "|"
    n_ellipses = timer
    log_interval = check_timer / n_ellipses
    for n in range(n_ellipses):
        single_interval = log_interval / 3
        await sleep(single_interval)
        bars += "="
        disp = bars + ">"
        if n == n_ellipses - 1:
            disp += "|"
        print(disp)


# -- base models --

class BaseModel(_BaseModel):
    """Base Pydantic Model with custom app configuration"""
    model_config = ConfigDict(arbitrary_types_allowed=True)


@dataclass
class BaseClass:
    """Base Python Dataclass multipurpose class with custom app configuration."""
    def to_dict(self):
        return asdict(self)


class JobStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class DatabaseCollections(Enum):
    PENDING_JOBS = "PENDING_JOBS".lower()
    IN_PROGRESS_JOBS = "IN_PROGRESS_JOBS".lower()
    COMPLETED_JOBS = "COMPLETED_JOBS".lower()


class MultipleConnectorError(Exception):
    def __init__(self, message: str):
        self.message = message


# -- jobs --

class Job(BaseModel):
    job_id: str
    status: str
    timestamp: str
    comparison_id: str


class InProgressJob(Job):
    job_id: str
    status: str
    timestamp: str
    comparison_id: str
    worker_id: str


class CompletedJob(Job):
    job_id: str
    status: str
    timestamp: str
    comparison_id: str
    results: Dict


class DatabaseConnector(ABC):
    """Abstract class that is both serializable and interacts with the database (of any type). """
    def __init__(self, connection_uri: str, database_id: str, connector_id: str):
        self.database_id = database_id
        self.client = self._get_client(connection_uri)
        self.db = self._get_database(self.database_id)

    @staticmethod
    def timestamp() -> str:
        return str(datetime.utcnow())

    def refresh_jobs(self):
        def refresh_collection(coll):
            for job in self.db[coll].find():
                self.db[coll].delete_one(job)

        for collname in ['completed_jobs', 'in_progress_jobs', 'pending_jobs']:
            refresh_collection(collname)

    @abstractmethod
    def _get_client(self, *args):
        pass

    @abstractmethod
    def _get_database(self, db_id: str):
        pass

    @abstractmethod
    def pending_jobs(self):
        pass

    @abstractmethod
    def completed_jobs(self):
        pass

    @abstractmethod
    async def read(self, *args, **kwargs):
        pass

    @abstractmethod
    async def write(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_collection(self, **kwargs):
        pass


class MongoDbConnector(DatabaseConnector):
    def __init__(self, connection_uri: str, database_id: str, connector_id: str = None):
        super().__init__(connection_uri, database_id, connector_id)

    def _get_client(self, *args):
        return MongoClient(args[0])

    def _get_database(self, db_id: str) -> Database:
        return self.client.get_database(db_id)

    def _get_jobs_from_collection(self, coll_name: str):
        return [job for job in self.db[coll_name].find()]

    def pending_jobs(self):
        return self._get_jobs_from_collection("pending_jobs")

    def completed_jobs(self):
        return self._get_jobs_from_collection("completed_jobs")

    async def read(self, collection_name: DatabaseCollections | str, **kwargs):
        """Args:
            collection_name: str
            kwargs: (as in mongodb query)
        """
        coll_name = self._parse_enum_input(collection_name)
        coll = self.get_collection(coll_name)
        result = coll.find_one(kwargs.copy())
        return result

    async def write(self, collection_name: DatabaseCollections | str, **kwargs):
        """
            Args:
                collection_name: str: collection name in mongodb
                **kwargs: mongo db `insert_one` query defining the document where the key is as in the key of the document.
        """
        coll_name = self._parse_enum_input(collection_name)

        for k in kwargs.keys():
            v = kwargs[k]
            kwargs[k] = self._parse_enum_input(v)

        coll = self.get_collection(coll_name)
        result = coll.insert_one(kwargs.copy())
        return kwargs

    def get_collection(self, collection_name: str) -> Collection:
        try:
            return self.db[collection_name]
        except:
            return None

    async def insert_job_async(self, collection_name: str, **kwargs) -> Dict[str, Any]:
        return self.insert_job(collection_name, **kwargs)

    def insert_job(self, collection_name: str, **kwargs) -> Dict[str, Any]:
        coll = self.get_collection(collection_name)
        job_doc = kwargs
        coll.insert_one(job_doc)
        return job_doc

    async def update_job_status(self, collection_name: str, job_id: str, status: str | JobStatus):
        job_status = self._parse_enum_input(status)
        return self.db[collection_name].update_one({'job_id': job_id, }, {'$set': {'status': job_status}})

    def _parse_enum_input(self, _input: Any) -> str:
        return _input.value if isinstance(_input, Enum) else _input
