import sys
from dotenv import dotenv_values
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine.base import Engine



def main():

    commands = {'create':create_all, 'drop':drop_all, 'reset':reset,}

    try:
        commands[sys.argv[1]]()
    except:
        print('no or invalud arg(s) provided')

    

def drop_all(meta: MetaData, engine: Engine) -> None:
    meta.drop_all(engine)

def create_all(meta: MetaData, engine: Engine) -> None:
    meta.create_all(engine)

def reset():
    print('reset called')


if __name__ == '__main__':
    main()