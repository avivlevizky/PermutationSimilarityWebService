import atexit

import click_spinner
import typer
from pathlib import Path

from uvicorn import Server, Config
from confuse import Configuration

from app.core.asyncio import EventLoopBase
from app.core.containers import container
from app.core.errors_handling import async_func_error_handler
from app.db.mongodb.client import AsyncMongoDBBaseClient
from app.db.mongodb.util import AsyncMongoDBUtil
from app.main import fastapi_app
from app.services.terms import TermsService

CLI_APP = typer.Typer()


@async_func_error_handler
@CLI_APP.command()
def create_db_collections():
    typer.echo("Creating db collections")
    event_loop = container[EventLoopBase]
    with click_spinner.spinner():
        event_loop.run(container[AsyncMongoDBUtil].create_indexes())


@async_func_error_handler
@CLI_APP.command()
def process_data_from_file_to_db(file_path: str):
    typer.echo(f"Starting to process data from file: {file_path}")
    event_loop = container[EventLoopBase]
    terms_service = container[TermsService]
    with click_spinner.spinner():
        total_terms_inserted = event_loop.run(terms_service.process_data_from_path_by_chunk(Path(file_path)))
    typer.echo(f"Successfully processed and inserted {total_terms_inserted} terms from file to DB!")


@async_func_error_handler
@CLI_APP.command()
def runserver():
    typer.echo("Starting server...")
    config = container[Configuration]
    event_loop = container[EventLoopBase]
    hostname = config['app']['hostname']
    port = config['app']['port']
    server_config = Config(app=fastapi_app, host=hostname, port=port, loop=event_loop.get_loop())
    uvicorn_server = Server(server_config)
    event_loop.run(uvicorn_server.serve())


def close_cleanup():
    container[AsyncMongoDBBaseClient].close()


if __name__ == "__main__":
    atexit.register(close_cleanup)
    CLI_APP()
