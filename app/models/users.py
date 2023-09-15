from app.config.db_config import Base
from app.models.base import CommonBase
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from app.models.groups import user_group_membership
from app.models.roles import user_role_membership


class User(Base, CommonBase):
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String, nullable=False)
    date_created = Column(DateTime(timezone=False), default=datetime.utcnow())
    password = Column(String)
    roles = relationship("Role", secondary=user_role_membership, back_populates="users")
    groups = relationship("Group", secondary=user_group_membership, back_populates="users")
