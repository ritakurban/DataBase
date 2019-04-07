# Install all necessary packages
import sqlalchemy
from sqlalchemy import create_engine, Column, Text, Integer, ForeignKey, DateTime, DECIMAL, VARCHAR, func, and_, text, case, Date, cast
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import time
from datetime import date
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
import pandas as pd
import numpy as np
from datetime import datetime

# Create and connect the engine
engine = create_engine('sqlite:///database.db')
engine.connect()

Base = declarative_base()

# Build tables
class Agents(Base):
    __tablename__ = 'agents'
    ID = Column(Integer, primary_key=True, index=True)
    name = Column(Text)
    email = Column(Text)

    def __repr__(self):
        return "<Agent(id={0}, name={1} email={2}>".format(self.ID, self.name, self.email)

class Buyers(Base):
    __tablename__ = 'buyers'
    ID = Column(Integer, primary_key=True, index=True)
    name = Column(Text)
    email = Column(Text)

    def __repr__(self):
        return "<Buyer(id={0}, name={1}, email={2}>".format(self.ID, self.name, self.email)

class Sellers(Base):
    __tablename__ = 'sellers'
    ID = Column(Integer, primary_key=True, index=True)
    name = Column(Text)
    email = Column(Text)

    def __repr__(self):
        return "<Seller(id={0}, name={1}, email={2}>".format(self.ID,self.name, self.email)

class Offices(Base):
    __tablename__ = 'offices'
    ID = Column(Integer, primary_key=True, index=True)
    name = Column(Text)

    def __repr__(self):
        return "<Seller(id={0}, name={1}>".format(self.ID, self.name)


class Houses(Base):
    __tablename__ = 'houses'
    ID = Column(Integer, primary_key = True, index=True)
    seller_id = Column(Integer, ForeignKey('sellers.ID'))
    n_bedrooms = Column(Integer)
    n_bathrooms = Column(Integer)
    price = Column(Integer)
    zip_code = Column(Integer) #should it be ID?
    date = Column(DateTime)
    agent_id = Column(Integer, ForeignKey('agents.ID'))
    office_id = Column(Integer, ForeignKey('offices.ID')) #potentially combine with zips
    status =Column(Integer)



    def __repr__(self):
        return "<House(id={0}, seller_id={1}, n_bedrooms={2},\
        n_bathrooms={3}, price={4}, zip_code={5}, date={6}, \
        agent_id={7}, office_id={8}, status={9})>".format(self.ID, self.seller_id, self.n_bedrooms,
                                                          self.n_bathrooms, self.price, self.zip_code,
                                                          self.date, self.agent_id, self.office_id, self.status)

class Sales(Base):
    __tablename__ = 'sales'
    ID = Column(Integer, primary_key = True, index=True)
    house_id = Column(Integer, ForeignKey('houses.ID'))
    buyer_id = Column(Integer, ForeignKey('buyers.ID'))
    sale_price = Column(Integer)
    date = Column(DateTime)

    def __repr__(self):
        return "<Sale(id={0}, house_id={1}, buyer_id={2}, sale_price={3}, date={4}>".format(self.ID,
                                                                                            self.house_id,
                                                                                            self.buyer_id,
                                                                                            self.sale_price,
                                                                                            self.date)



class Commissions(Base):
    __tablename__ = 'commissions'
    ID = Column(Integer, primary_key = True, index=True)
    sale_id = Column(Integer, ForeignKey('sales.ID'))
    amount = Column(Integer)
    agent_id = Column(Text)


    def __repr__(self):
        return "<Commissions(id = {0}, sale_id={1}, amount={2}, agent_id={3}>".format(self.ID,
                                                                                      self.sale_id,
                                                                                      self.amount,
                                                                                      self.agent_id)
