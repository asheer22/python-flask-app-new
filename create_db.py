import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the database URL (without the database name) and the database name
db_url = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
db_name = os.getenv('DB_NAME')


# Create an engine to connect to the MySQL server
engine = create_engine(db_url)

# Connect to the MySQL server and create the database
try:
    with engine.connect() as connection:
        query = text("CREATE DATABASE IF NOT EXISTS {db_name}")
        result = connection.execute(query)
        print(f"Database '{db_name}' created or already exists.")
except OperationalError as e:
    print(f"Error creating database: {e}")
