import sys
from dotenv import dotenv_values
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine.base import Engine
import models


def main():
    
    commands = {'create':create_all, 'drop':drop_all, 'reset':reset, 'populate':create_dummy_data}

    try:
        config = dotenv_values()
        connection_string = f'postgresql+psycopg2://{config["USERNAME"]}:{config["PASSWORD"]}@{config["HOST"]}:{config["PORT"]}/{config["DATABASE"]}'
        print(connection_string)

        engine = create_engine(connection_string, echo=False)
        commands[sys.argv[1]](models.Base.metadata,engine)
    except Exception as e:
        print('error')
        print(e.with_traceback)


def drop_all(meta: MetaData, engine: Engine) -> None:
    meta.drop_all(engine)


def create_all(meta: MetaData, engine: Engine) -> None:
    meta.create_all(engine)

def create_dummy_data(meta: MetaData, engine: Engine) -> None:

    print('dummy data created')

def reset(meta: MetaData, engine: Engine):
    meta.drop_all(engine)
    meta.create_all(engine)
    create_dummy_data(meta, engine)

if __name__ == '__main__':
    main()