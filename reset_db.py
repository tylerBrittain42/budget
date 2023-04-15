from sqlalchemy import text
from sqlalchemy import create_engine
from dotenv import dotenv_values

config = dotenv_values()
connection_string = f'mysql+mysqlconnector://{config["USERNAME"]}:{config["PASSWORD"]}@{config["HOST"]}:{config["PORT"]}/{config["DATABASE"]}'
print(connection_string)

file = open('sql_scripts/foo.sql')

engine = create_engine(connection_string, echo=True)
with engine.connect() as connection:
    connection.execute()
