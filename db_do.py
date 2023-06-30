import sys
from dotenv import dotenv_values
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Engine
from models import models


def main():
    
    commands = {'create': create_all, 'drop': drop_all, 'reset': reset, 'populate': create_dummy_data}

    # try:
    config = dotenv_values()
    # print(connection_string)
    if len(sys.argv) > 2:
        print(f'using {sys.argv[2]}')
        connection_string = sys.argv[2]
    else:
        print('using postgres db')
        connection_string = f'postgresql+psycopg2://{config["USERNAME"]}:{config["PASSWORD"]}@{config["HOST"]}:{config["PORT"]}/{config["DATABASE"]}'

    engine = create_engine(connection_string, echo=False)
    commands[sys.argv[1]](models.Base.metadata, engine)
    # except Exception as e:
    # print('error')
    # print(e.with_traceback)


def drop_all(meta: MetaData, engine: Engine) -> None:
    print('Dropping data')
    meta.drop_all(engine)
    print('Data has been  dropped.')


def create_all(meta: MetaData, engine: Engine) -> None:
    print('Creating tables')
    meta.create_all(engine)
    print('Tables have been created')


def create_dummy_data(meta: MetaData, engine: Engine) -> None:
    print('Creating dummy data')

    session = Session(engine)
    user = models.User(name='test_user_1')
    session.add(user)
    income_1 = models.Income(amount=500, u_id=1)
    session.add(income_1)
    session.commit()

    print('Dummy data has been created')


def reset(meta: MetaData, engine: Engine):
    meta.drop_all(engine)
    meta.create_all(engine)
    create_dummy_data(meta, engine)


if __name__ == '__main__':
    main()
