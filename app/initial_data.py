import logging


from app.config.init_db import init_db
from app.config.session import SessionLocal


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




def init() -> None:
    db = SessionLocal()
    init_db(db)

def main() -> None:
    logger.info("Starting initial data process...")
    init()
    logger.info("Initial data process finished.")


if __name__ == "__main__":
    main()
