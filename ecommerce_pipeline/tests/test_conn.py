import os
import unittest

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# environment variables
load_dotenv(str(os.getenv("PWD"))+"/.env.dev")

class TestPostgresConnection(unittest.TestCase):
    def test_connection(self):
        # Retrieve connection information from environment variables
        db_driver = os.getenv("DB_DRIVER")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")

        # Create a connection string for SQLAlchemy
        conn_string = f"{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        print(conn_string)
        # Try to connect to the database using SQLAlchemy
        try:
            engine = create_engine(conn_string)
            with engine.connect():
                print("Successfully connected to the database")
        except OperationalError as e:
            self.fail(f"Could not connect to the database: {str(e)}")