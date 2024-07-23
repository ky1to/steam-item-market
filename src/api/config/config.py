import os
from dotenv import load_dotenv

path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')

load_dotenv(path)

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')