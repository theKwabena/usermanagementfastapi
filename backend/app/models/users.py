from app.config.db_config import Base
from app.models.base import CommonBase
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.models.groups import user_group_membership
from app.models.roles import user_role_membership


class User(Base, CommonBase):
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String)
    phone_number = Column(String, nullable=True)
    password = Column(String)
    profile_img = Column(String, default="static/users/default_profile.png")

    email_verified = Column(Boolean, default=False)
    auth_identity_provider = Column(String(255))

    is_superuser = Column(Boolean, default = False)
    date_created = Column(DateTime(timezone=False), default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)

    roles = relationship("Role", secondary=user_role_membership, back_populates="users")
    groups = relationship("Group", secondary=user_group_membership, back_populates="users")
