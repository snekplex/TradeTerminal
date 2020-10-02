import uuid
import datetime
from typing import Dict
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer(), ForeignKey('user.id', ondelete='CASCADE'))
    uuid =  Column(String(), unique=True, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    name = Column(String(32), unique=False, nullable=False)
    balance =  Column(Float(), default=100000.00, nullable=False)
    position_ids = Column(Integer, ForeignKey('position.id', ondelete='CASCADE'))
    positions = relationship('Position', cascade='all,delete', backref='account', foreign_keys=[])
    # user - Relationship from User

    def __repr__(self):
        return '<Account: id={} | name={} | balance={}/>'.format(self.id, self.name, self.balance)

    @property
    def serialize(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'balance': self.balance
        }

    def remove_from_balance(self, amount: float) -> bool:
        new_balance = self.balance - amount
        if new_balance < 0.00:
            return False
        else:
            self.balance = new_balance
            return True

