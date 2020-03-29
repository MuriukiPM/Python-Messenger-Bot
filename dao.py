from libs import DBOrders, DBUsers
from sqlalchemy.orm import sessionmaker, load_only
from sqlalchemy import create_engine, and_
import sys
import logging as log
from sqlalchemy.sql import func
from os import environ as env
from dotenv import load_dotenv

load_dotenv()
creds = ['DB_USER','DB_HOST','DB_NAME','DB_PASS','DB_PORT']
if not all([cred in env for cred in creds]): 
    log.error('Be sure to set all environment vars')
    sys.exit(1)
DB_USER = env.get('DB_USER')
DB_HOST = env.get('DB_HOST')
DB_NAME = env.get('DB_NAME')
DB_PASS = env.get('DB_PASS')
DB_PORT = env.get('DB_PORT')
engine = create_engine('postgresql://{0}:{1}@{2}:{3}/{4}'.format(DB_USER,DB_PASS,DB_HOST,DB_PORT,DB_NAME),
                        echo=True, pool_pre_ping=True)  
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()
try:
    version = session.execute("SELECT version()")
    log.warn(version.fetchall())
except:
    log.error('Could not create db engine')
    sys.exit(1) 

def create_user_by_messenger(messenger_id: str, first_name: str, last_name: str, age: int = None, gender: str = None):
    session.add(DBUsers(messenger_id=messenger_id,
                        first_name=first_name,
                        last_name=last_name
                        )
                )
    session.commit()

def update_user_by_messenger(messenger_id: str, first_name: str = None, last_name: str = None, age: int = None, gender: str = None):
    payload, cols = {}, {'first_name':first_name, 'last_name':last_name, 'age':age, 'gender':gender}
    for key, value in cols.items(): 
        if value is not None: payload[key] = value
    session.query(DBUsers) \
            .filter(DBUsers.messenger_id==messenger_id) \
            .update(payload)
    session.commit()

def find_user_by_messenger_id(messenger_id: str):
    return session.query(DBUsers) \
        .filter(DBUsers.messenger_id == messenger_id) \
        .first()