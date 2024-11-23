import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_DSN=os.getenv("POSTGRES_DSN")
MINIO_ADDR=os.getenv("MINIO_ADDR")

DB_NAME=os.getenv("DB_NAME")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
S3_ADMIN=os.getenv("S3_ADMIN")
S3_PASSWORD=os.getenv("S3_PASSWORD")
SECRET_KEY=os.getenv("SECRET_KEY")
