from fastapi import FastAPI

from shared.data_model import DbClientResponse
from shared.database import DatabaseConnector
from shared.environment import DEFAULT_DB_TYPE


def check_client(db_connector: DatabaseConnector) -> DbClientResponse:
    """TODO: generalize this to work with multiple client types. Currently using Mongo."""
    msg = "Pinged your deployment. You successfully connected to MongoDB!"
    status = "PASS"
    try:
        db_connector.client.admin.command('ping')
    except Exception as e:
        msg = f"Failed to connect to MongoDB:\n{e}"
        status = "FAIL"
    return DbClientResponse(
        message=msg,
        db_type=DEFAULT_DB_TYPE,
        timestamp=db_connector.timestamp(),
        status=status
    )


def stop_client(db_connector: DatabaseConnector) -> DbClientResponse:
    """TODO: generalize this to work with multiple client types. Currently using Mongo."""
    db_connector.client.close()

    return DbClientResponse(
        message=f"{DEFAULT_DB_TYPE} successfully closed!",
        db_type=DEFAULT_DB_TYPE,
        timestamp=db_connector.timestamp()
    )

