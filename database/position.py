import uuid
import datetime
from typing import Dict
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from database import Base

class Position(Base):
    __tablename__ = 'position'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer(), ForeignKey('account.id', ondelete='CASCADE'))
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    buy_price = Column(Float(), nullable=False)
    ticker = Column(String(), nullable=False)
    shares = Column(Integer(), nullable=False)
    # account - Relationship from Account

    def __repr__(self):
        return '<Position: ticker={} | shares={} @ ${} />'.format(self.ticker, self.shares, 
                                                                         self.buy_price)

    @property
    def serialize(self) -> Dict:
        return {
            'id': self.id,
            'ticker': self.ticker,
            'shares': self.shares,
            'buy_price': self.buy_price
        }


