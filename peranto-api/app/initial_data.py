import logging
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)


from app.db.init_db import init_db
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def init() -> None:
    db = SessionLocal()
    init_db(db)

def main() -> None:
    logger.info("Creating initial data...")
    init()
    logger.info("Initial data created.")

if __name__ == "__main__":
    main()