# Import all models to base before imported by alembic

from app.config.db_config import Base
from app.models.users import User
from app.models.groups import Group
from app.models.roles import Role