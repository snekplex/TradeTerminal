from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)
session = Session()
meta = MetaData()

meta.create_all(engine)