import pytest
import os
from sqlalchemy import create_engine, text
from models import models

connection_string = 'sqlite:///tests/db.sqlite'


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

        os.system(f'python db_do.py create {connection_string}')
        with self.engine.connect() as conn:
            results = conn.execute(text('select * from sqlite_master'))
        assert len(results.all()) == self.EXPECTED_TABLES

    def test_drop(self):
        # confirming db has not been emptied
        with self.engine.connect() as conn:
            results = conn.execute(text('select * from sqlite_master'))
        assert len(results.all()) != 0

        os.system(f'python db_do.py drop {connection_string}')
        with self.engine.connect() as conn:
            results = conn.execute(text('select * from sqlite_master'))
        assert len(results.all()) == 0

    def test_reset(self, database_clear):
        # confirming db has not been emptied
        with self.engine.connect() as conn:
            results = conn.execute(text('select * from sqlite_master'))
        assert len(results.all()) == 0

        os.system(f'python db_do.py reset {connection_string}')
        with self.engine.connect() as conn:
            results = conn.execute(text('select * from sqlite_master'))
        assert len(results.all()) == self.EXPECTED_TABLES

        return

    def test_populate(self, database_create_tables):
        # expected output
        EXPECTED_USER = {
                'name': 'test_user_1',
                }
        EXPECTED_INCOME = {
                'amount': 500
                }
        # confirming db has not been emptied
        with self.engine.connect() as conn:
            results = conn.execute(text('select * from sqlite_master'))
        assert len(results.all()) != 0

        os.system(f'python db_do.py populate {connection_string}')
        with self.engine.connect() as conn:
            user_result = conn.execute(text("select * from User")).one()
            income_result = conn.execute(text("select * from Income")).one()
            print(user_result.name)

        assert user_result.name == EXPECTED_USER['name']
        assert income_result.amount == EXPECTED_INCOME['amount']
        # assert user_results is None
        return
