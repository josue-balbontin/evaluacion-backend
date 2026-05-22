import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from logging import config as logging_config
from core.logger import LOGGING

# Apply logging settings
logging_config.dictConfig(LOGGING)

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', '.env'))

load_dotenv(dotenv_path=ENV_PATH, override=False)

# Project name. Used in Swagger documentation
PROJECT_NAME = os.getenv('PROJECT_NAME', 'FastAPI Application')

# Redis settings
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))


# Postgres settings
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', 5432))
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

_db_password = quote_plus(DB_PASSWORD)
POSTGRES_URL = f'postgresql://{DB_USER}:{_db_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
POSTGRES_DSN = (
    f"dbname='{DB_NAME}' user='{DB_USER}' password='{DB_PASSWORD}' "
    f"host='{DB_HOST}' port='{DB_PORT}'"
)