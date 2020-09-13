import uuid
import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)

    def __repr__(self):
        return '<Account: id={} | name={} />'.format(self.id, self.name)