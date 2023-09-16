# Import all models to base before imported by alembic

from app.config.db_config import Base # noqa
from app.models.users import User # noqa
from app.models.groups import Group # noqa
from app.models.roles import Role # noqa