from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint  # <- SQLAlchemy types here

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)         # Integer (not int)
    email: Mapped[str] = mapped_column(String, unique=True, index=True) # String (not str)
    hashed_password: Mapped[str] = mapped_column(String)
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")

class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)         # Integer
    name: Mapped[str] = mapped_column(String, unique=True)             # String

class UserRole(Base):
    __tablename__ = "user_roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)         # Integer (not int)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))       # ForeignKey is correct
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    user = relationship("User", back_populates="roles")
    role = relationship("Role")

    __table_args__ = (UniqueConstraint("user_id", "role_id"),)
