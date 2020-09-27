import uuid
import bcrypt
import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    uuid =  Column(String(), unique=True, nullable=False)
    username = Column(String(32), unique=True, nullable=False)
    password_hash = Column(String())
    account_ids = Column(Integer, ForeignKey('account.id', ondelete='CASCADE'))
    accounts = relationship('Account', cascade='all,delete', backref='user', foreign_keys=[account_ids])

    def __repr__(self):
        return '<User: id={} | name={} />'.format(self.id, self.name)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
        }

    @property
    def password(self):
        raise AttributeError('Password Security. Password not available')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf=8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))