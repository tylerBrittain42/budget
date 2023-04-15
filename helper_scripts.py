from dotenv import dotenv_values
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine.base import Engine
from models import User, Base


def main():

    # Creating engine and metadata
    config = dotenv_values()
    connection_string = f'mysql+mysqlconnector://{config["USERNAME"]}:{config["PASSWORD"]}@{config["HOST"]}:{config["PORT"]}/{config["DATABASE"]}'
    engine = create_engine(connection_string, echo=True)
    

    create_all(Base.metadata, engine)

    # drop_all(metadata_obj, engine)
    

def drop_all(meta: MetaData, engine: Engine) -> None:
    meta.drop_all(engine)

def create_all(meta: MetaData, engine: Engine) -> None:
    meta.create_all(engine)


if __name__ == '__main__':
    main()