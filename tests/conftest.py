import pytest
import psycopg  
from config import DATABASE_CONFIG


@pytest.fixture
def conn():
    connection = psycopg.connect(**DATABASE_CONFIG)
    yield connection
    connection.close()


@pytest.fixture
def compter(conn):
    def _compter(requete):
        cursor = conn.cursor()
        cursor.execute(requete)
        return cursor.fetchone()[0]
    return _compter