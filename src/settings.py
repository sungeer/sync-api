import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.engine import URL

VERSION = '26.1119.1542'

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = BASE_DIR / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)


ENVIRONMENTS = ('development', 'testing', 'production')
ENVIRONMENT = os.getenv('ENVIRONMENT')
if ENVIRONMENT not in ENVIRONMENTS:
    raise ValueError(f'Invalid ENVIRONMENT: {ENVIRONMENT}')

# LOG_FILE = BASE_DIR / 'logs/hostess.log'
LOG_DIR = Path(os.getenv('LOG_DIR', default=str(BASE_DIR / 'logs')))

DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT', default='3306'))
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_URL = URL.create(
    drivername='mysql+pymysql',
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)
