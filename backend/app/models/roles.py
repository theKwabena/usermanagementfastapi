from sqlalchemy import Column, Table, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.config.db_config import Base

from app.models.groups import group_role_membership


user_role_membership = Table(
    "user_role_membership",
    Base.metadata,
Column('user_id', UUID, ForeignKey('user.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey("role.id"), primary_key=True)
)


class Role(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,unique=True,  index=True)
    groups = relationship("Group", secondary=group_role_membership, back_populates="roles")
    users = relationship("User", secondary=user_role_membership, back_populates="roles")