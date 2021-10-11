import atexit
from typing import NoReturn

import click_spinner
import typer
from pathlib import Path

from uvicorn import Server, Config
from confuse import Configuration

from app.core.asyncio import EventLoopBase
from app.core.containers import container
from app.core.errors_handling import async_func_error_handler_logging
from app.db.mongodb.client import AsyncMongoDBBaseClient
from app.db.mongodb.util import AsyncMongoDBUtils
from app.main import fastapi_app
from app.services.words import WordsService

CLI_APP = typer.Typer()


@async_func_error_handler_logging
@CLI_APP.command()
def create_db_collections():
    """
    CLI command for creating and indexing the necessary databases collections
    """
    db_name = container[Configuration]['mongodb']['db_name'].get()
    typer.echo(f"Creating mongodb collections in {db_name} database")
    event_loop = container[EventLoopBase]
    with click_spinner.spinner():
        event_loop.run(container[AsyncMongoDBUtils].create_indexes(db_name))


@async_func_error_handler_logging
@CLI_APP.command()
def process_data_from_file_to_db(file_path: str):
    """
    CLI command for process and store the dictionary data from file
    :param file_path: The dictionary data file
    """
    typer.echo(f"Starting to process data from file: {file_path}")
    event_loop = container[EventLoopBase]
    words_service = container[WordsService]
    with click_spinner.spinner():
        total_words_inserted = event_loop.run(words_service.process_data_from_path_by_chunk(Path(file_path)))
    typer.echo(f"Successfully processed and inserted {total_words_inserted} words from file to DB!")


@async_func_error_handler_logging
@CLI_APP.command()
def runserver():
    """
    CLI command for running the webserver(uvicorn) and the webservice application(FastAPI)
    """
    typer.echo("Starting server...")

    # Webserver config settings
    config = container[Configuration]
    event_loop = container[EventLoopBase]
    hostname = config['app']['hostname'].get()
    port = config['app']['port'].get()
    # Webservice application
    app = fastapi_app
    server_config = Config(app=app, host=hostname, port=port, loop=event_loop.get_loop())

    # Initialize the webserver
    uvicorn_server = Server(server_config)
    event_loop.run(uvicorn_server.serve())


def close_cleanup() -> NoReturn:
    """
    Resources Cleanup handler
    """
    container[AsyncMongoDBBaseClient].close()


if __name__ == "__main__":
    atexit.register(close_cleanup)
    CLI_APP()
