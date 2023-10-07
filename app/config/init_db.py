import logging
from sqlalchemy.orm import Session

from app.crud.user import user as user_db
from app.crud.permissions import group as group_db
from app.schemas.user import UserCreate
from fastapi import HTTPException
from app.schemas.permissions import GroupCreate
from app.config.settings import settings


# from app.db import base # noqa: F401


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    logger.info('Checking if first admin user exists...')
    user = user_db.get_by_email(db, email=settings.FIRST_ADMIN)
    if not user:
        logger.info('Admin user does not exist, Creating admin user...')
        user_in = UserCreate(
            first_name = "admin",
            last_name = "admin",
            email=settings.FIRST_ADMIN,
            password=settings.FIRST_ADMIN_PASSWORD,
            is_superuser=True,
        )
        user = user_db.create(db, obj_in=user_in)  # noqa: F841
    else :
        logger.info("Admin user exists, proceeding...")