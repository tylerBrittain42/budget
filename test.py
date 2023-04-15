from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from dotenv import dotenv_values


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    
config = dotenv_values()
connection_string = f'mysql+mysqlconnector://{config["USERNAME"]}:{config["PASSWORD"]}@{config["HOST"]}:{config["PORT"]}/{config["DATABASE"]}'
print(connection_string)

engine = create_engine(connection_string, echo=True)
with engine.connect() as connection:
    connection.execute(text("CREATE TABLE example (id INTEGER, name VARCHAR(20))"))
