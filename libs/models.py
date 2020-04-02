from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, String, BigInteger, Boolean 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
Base = declarative_base()

class DBUsers(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    # messenger_id = Column(BigInteger)
    messenger_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime,  onupdate=func.now())
    age = Column(String, default='')
    gender = Column(String, default='')

class DBOrders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    is_complete = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime,  onupdate=func.now())
    # user = relationship(DBUsers)
