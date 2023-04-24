import sys
from dotenv import dotenv_values
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine.base import Engine
import models


def main():


    commands = {'create':create_all, 'drop':drop_all, 'reset':reset,}

    try:
        config = dotenv_values()
        connection_string = f'mysql+mysqlconnector://{config["USERNAME"]}:{config["PASSWORD"]}@{config["HOST"]}:{config["PORT"]}/{config["DATABASE"]}'
        print(connection_string)

        engine = create_engine(connection_string, echo=True)
        commands[sys.argv[1]](models.Base.metadata,engine)
    except Exception as e:
        print(e)

    

def drop_all(meta: MetaData, engine: Engine) -> None:
    meta.drop_all(engine)

def create_all(meta: MetaData, engine: Engine) -> None:
    meta.create_all(engine)

def reset():
    print('reset called')


if __name__ == '__main__':
    main()