from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from database import Base

engine = create_engine('sqlite:///app.db')

if not database_exists(engine.url):
    create_database(engine.url)
    Base.metadata.create_all(engine, checkfirst=True)

Session = sessionmaker(bind=engine)
session = Session()
meta = MetaData()
