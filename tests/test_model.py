import pytest
import os
from sqlalchemy import create_engine, text
from models import models

connection_string = 'sqlite:///tests/db.sqlite'
# TODO change 'a' to connection string. Adjust script to read input for connection string

@pytest.fixture
def database_clear():
    engine = create_engine(connection_string, echo=False)
    models.Base.metadata.drop_all(engine)

    # with engine.connect() as conn:
    #     results = conn.execute(text('select name from sqlite_master'))
    #     for table in results.all():
    #         conn.execute(text(f'drop table {table[0]}'))

    return


@pytest.fixture
def database_create_tables(database_clear):
    engine = create_engine(connection_string, echo=False)
    models.Base.metadata.create_all(engine)
    return


# Note: using raw SQL to validate script
class TestDbDo:
    engine = create_engine(connection_string, echo=False)
    EXPECTED_TABLES = 7

    def test_create(self, database_clear):
        # confirming db has been emptied
        with self.engine.connect() as conn:
            results = conn.execute(text('select * from sqlite_master'))
        assert len(results.all()) == 0

        os.system("python db_do.py create a")
        with self.engine.connect() as conn:
            results = conn.execute(text('select * from sqlite_master'))
        assert len(results.all()) == self.EXPECTED_TABLES

    def test_drop(self):
        # confirming db has not been emptied
        with self.engine.connect() as conn:
            results = conn.execute(text('select * from sqlite_master'))
        assert len(results.all()) != 0

        os.system("python db_do.py drop a")
        with self.engine.connect() as conn:
            results = conn.execute(text('select * from sqlite_master'))
        assert len(results.all()) == 0

    def test_reset(self, database_clear):
        # confirming db has not been emptied
        with self.engine.connect() as conn:
            results = conn.execute(text('select * from sqlite_master'))
        assert len(results.all()) == 0

        os.system("python db_do.py reset a")
        with self.engine.connect() as conn:
            results = conn.execute(text('select * from sqlite_master'))
        assert len(results.all()) == self.EXPECTED_TABLES

        #TODO add populate test

        return

    def populate(self, data):
        return