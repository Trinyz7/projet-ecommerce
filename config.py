import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "ecommerce"),
        "user": os.getenv("DB_USER", "groupe_2"),
    "password": os.getenv("DB_PASSWORD", "tp_grp_2"),
}