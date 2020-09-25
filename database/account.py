import uuid
import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base

class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    uuid =  Column(String(), unique=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    balance =  Column(Float(), default=100000.00, nullable=False)
    # user - Relationship from User

    def __repr__(self):
        return '<Account: id={} | name={} />'.format(self.id, self.name)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'balance': self.balance
        }



