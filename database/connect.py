from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

engine = create_engine('sqlite:///app.db')

if not database_exists(engine.url):
    create_database(engine.url)

Session = sessionmaker(bind=engine)
session = Session()
meta = MetaData()

meta.create_all(engine)