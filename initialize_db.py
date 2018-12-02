from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common.const import OBJECT_NUMBERS, CONSTRAINTS
from common.ships import populate_database

engine = create_engine('sqlite:///Ships.db')
Session = sessionmaker(bind=engine)

# create a Session
dbsession = Session()

populate_database(dbsession, OBJECT_NUMBERS, CONSTRAINTS)
