import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import DATE


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime.date: DATE
    }


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    income_sources: Mapped[list['Income']] = relationship(back_populates="user")
    ratios: Mapped[list['Ratio']] = relationship(back_populates="owner")
    subs: Mapped[list['Subscription']] = relationship(back_populates='')
    utilities: Mapped[list['Utility']] = relationship(back_populates='')
    line_items:Mapped[list['Line_item']] = relationship(back_populates='')

    def __repr__(self) -> str:
        return f'<user:{self.name}, id:{self.id}>'

    
class Income(Base):
    __tablename__ = 'income'
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date]
    amount: Mapped[int]
    u_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates="income_sources")

    def __repr__(self) -> str:
        return f'<income:{self.amount}, date:{self.date}>'


class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    type: Mapped[str] = mapped_column(String(30))

    # don't think I need to connect the relationship back
    def __repr__(self) -> str:
        return f'<category:{self.name}, id:{self.id}>'


class Ratio(Base):
    __tablename__ = 'ratio'

    # is the primary key line neccessary for this table?
    id: Mapped[int] = mapped_column(primary_key=True)
    # c_id: Mapped[int] 
    u_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    ratio: Mapped[float] 
    
    owner: Mapped['User'] = relationship(back_populates='ratios')
    type: Mapped['Category'] = relationship()

    def __repr__(self) -> str:
        return f'<ratio:{self.id} TBD>' #INCOMPLETE


class Utility(Base):
    __tablename__ = 'utility'
    id: Mapped[int] = mapped_column(primary_key=True)
    u_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    name: Mapped[str] = mapped_column(String(30))
    
    due_date: Mapped[datetime.date]
    cost: Mapped[float]
    paid: Mapped[bool]


    def __repr__(self) -> str:
        return f'<utility:{self.name}, amount:{self.cost}>'

# ie netflix, gym
class Subscription(Base):
    __tablename__ = 'subscription'
    id: Mapped[int] = mapped_column(primary_key=True)
    u_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    name: Mapped[str] = mapped_column(String(30))

    due_date: Mapped[datetime.date]
    cost: Mapped[float]
    paid: Mapped[bool]


    def __repr__(self) -> str:
        return f'<subscription:{self.name}, amount:{self.cost}>'

class Line_item(Base):
    __tablename__ = 'line_item'
    id: Mapped[int] = mapped_column(primary_key=True)
    u_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    name: Mapped[str] = mapped_column(String(30))

    date: Mapped[datetime.date]
    cost: Mapped[float]
    reason: Mapped[str] = mapped_column(String(30))
    # category_id: Mapped[int]
    

    def __repr__(self) -> str:
        return f'<line_item:{self.name} cost:{self.cost}'




