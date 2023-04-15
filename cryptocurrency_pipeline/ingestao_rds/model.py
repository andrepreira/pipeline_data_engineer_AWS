import os

from sqlite3 import Timestamp

from dotenv import load_dotenv
from sqlalchemy import create_engine,Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# environment variables
load_dotenv(str(os.getenv("PWD"))+"/env.dev")

DB_DRIVER = os.getenv("DB_DRIVER")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_TABLE_NAME = os.getenv("DB_TABLE_NAME")


Base = declarative_base()

class Coins(Base):
    __tablename__ = 'tb_coins'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    symbol = Column(String)
    data_added = Column(Text)
    last_updated = Column(Text)
    price = Column(Float)
    volume_24h = Column(Float)
    circulating_supply = Column(Float)
    total_supply = Column(Float)
    max_supply = Column(Float)
    volume_24h = Column(Float)
    percent_change_1h = Column(Float)
    percent_change_24h = Column(Float)
    percent_change_7d = Column(Float)
    
    def conn_engine():
        #postgres://{user}:{password}@{host}:{port}/{db_name}?sslmode=require
        db_string = "{driver}://{user}:{password}@{host}:{port}/{db_name}".format(
            driver = DB_DRIVER,
            user = DB_USER, 
            password = DB_PASSWORD, 
            host = DB_HOST, 
            port = DB_PORT, 
            db_name = DB_TABLE_NAME
        ) 
        return create_engine(db_string)
    
    def start():
        engine = Coins.conn_engine()
        Session = sessionmaker(engine)
        session = Session()
        Base.metadata.create_all(engine)
        print('\n Table created on database')
        return session, engine