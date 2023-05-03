import sys
from dotenv import dotenv_values
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine.base import Engine
import models
import psycopg2


def main():
    
    commands = {'create':create_all, 'drop':drop_all, 'reset':reset, 'populate':add_data}

    config = dotenv_values()
    connection_string = f'postgresql+psycopg2://{config["USERNAME"]}:{config["PASSWORD"]}@{config["HOST"]}:{config["PORT"]}/{config["DATABASE"]}'
    print(connection_string)

    engine = create_engine(connection_string )
    commands[sys.argv[1]](models.Base.metadata,engine)
   


def drop_all(meta: MetaData, engine: Engine) -> None:
    meta.drop_all(engine)


def create_all(meta: MetaData, engine: Engine) -> None:
    meta.create_all(engine)

def add_data(meta: MetaData, engine: Engine):
    print('NOT IMPLEMENTED')

def reset(meta: MetaData, engine: Engine):
    meta.drop_all(engine)
    meta.create_all(engine)


if __name__ == '__main__':
    main()