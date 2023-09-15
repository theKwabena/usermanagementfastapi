from sqlalchemy import Column, Table, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.config.db_config import Base


group_role_membership = Table(
    "groups_role_membership",
    Base.metadata,
    Column('group_id', Integer, ForeignKey("group.id"), primary_key=True),
    Column('role_id', Integer, ForeignKey("role.id"), primary_key=True)
)

user_group_membership = Table(
    "user_group_membership",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("group.id"), primary_key=True),
    Column("user_id", UUID, ForeignKey("user.id"), primary_key=True)
)

class Group(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    roles = relationship("Role", secondary=group_role_membership, back_populates="groups")
    users = relationship("User", secondary=user_group_membership,back_populates="groups" )


