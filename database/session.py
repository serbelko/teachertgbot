import logging
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Формирование строки подключения к БД
DATABASE_URL = f"postgresql+psycopg2://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.PORT}/{config.POSTGRES_DB}"

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.exception(f"Ошибка в зависимости get_db: {e}")
        raise e
    finally:
        db.close()
