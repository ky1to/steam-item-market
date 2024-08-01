import os
from dotenv import load_dotenv

load_dotenv()

AUTH_POSTGRES_USER = os.getenv('AUTH_POSTGRES_USER')
AUTH_POSTGRES_PASSWORD = os.getenv('AUTH_POSTGRES_PASSWORD')
AUTH_POSTGRES_DB = os.getenv('AUTH_POSTGRES_DB')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')