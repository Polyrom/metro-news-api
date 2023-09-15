import asyncio

import uvicorn

from api.app import app
from db.database import DataBase
from news_parser.parser import MetroNewsParser
from settings import get_settings

project_settings = get_settings()


def shutdown(parser_instance: MetroNewsParser, loop):
    parser_instance.stop_periodic_parsing()
    loop.stop()
    pending = asyncio.all_tasks()
    loop.run_until_complete(asyncio.gather(*pending))


async def create_and_gather_tasks(parser: MetroNewsParser, server: uvicorn.Server):
    parser_task = asyncio.create_task(parser.start_periodic_parsing())
    server_task = asyncio.create_task(server.serve())
    await asyncio.gather(parser_task, server_task)


if __name__ == '__main__':
    # initialize database
    db = DataBase(project_settings.sqlite_db)
    db.startup()
    # initialize parser task
    parser = MetroNewsParser(project_settings)
    # initialize server task
    server_config = uvicorn.Config(
        app=app,
        host=project_settings.host,
        port=project_settings.port
    )
    server = uvicorn.Server(server_config)
    try:
        asyncio.run(
            create_and_gather_tasks(parser, server)
        )
    except KeyboardInterrupt:
        pass
    finally:
        shutdown(parser, asyncio.get_event_loop())
