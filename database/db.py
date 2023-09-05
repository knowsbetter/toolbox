from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from server import config

engine = create_engine(config.DB_URL, echo=True)
session = Session(bind=engine)