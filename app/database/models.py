from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Tabela de associação entre usuários e grupos
user_group = Table(
    "user_group",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    groups = relationship("Group", secondary=user_group, back_populates="users")


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    users = relationship("User", secondary=user_group, back_populates="groups")
