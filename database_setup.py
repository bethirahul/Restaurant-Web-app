# Functions and variables used to manipulate different parts of python runtime
#   environment
import sys

# SQLAlchemy variables used in writing mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# To use in configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# To relate Foreign Key relationships
from sqlalchemy.orm import relationship

# To use in the configuration code at the end of configuration
from sqlalchemy import create_engine

# For Hashing passwords
from passlib.apps import custom_app_context


# Instance of the declarative base class
Base = declarative_base()
# ^^ Will let the SQLAlchemy know that out classes are special SQLAlchemy
#   classes that correspond to the tables in our database


# Classes (Tables)
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    user_id = Column(String(250), nullable=False)
    provider = Column(String(250), nullable=False)
    # ^^Google, Facebook, Local
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = custom_app_context.encrypt(password)
    
    def verify_password(self, password):
        custom_app_context.verify(password, self.password_hash)

    # Code to define what to send (in each restaurant) in JSON format
    @property
    def serialize(self):
        # Returns data in easily serializable format (like dictionary format)
        return {
            'name' : self.name,
            'id' : self.id,
            'email' : self.email,
            'picture' : self.picture,
            'user_id' : self.user_id,
            'provider' : self.provider
        }


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    creater_id = Column(String(250), ForeignKey('user.id'))
    creater = relationship(User)

    # Code to define what to send (in each restaurant) in JSON format
    @property
    def serialize(self):
        # Returns data in easily serializable format (like dictionary format)
        return {
            'name' : self.name,
            'id' : self.id,
            'creater_id' : self.creater_id
        }


class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
    creater_id = Column(String(80), ForeignKey('user.id'))
    creater = relationship(User)

    # Code to define what to send (in each item) in JSON format
    @property
    def serialize(self):
        # Returns data in easily serializable format (like dictionary format)
        return {
            'id' : self.id,
            'name' : self.name,
            'price' : self.price,
            'description' : self.description,
            'course' : self.course,
            'creater_id' : self.creater_id
        }


# Instance of create engine class and point to database we use
engine = create_engine('sqlite:///restaurantmenuwithusers.db')
# ^^ Above example has SQLite3 with database 'restaurant'

# This goes into database and creates all the classes we will soon create as
#   new tables
Base.metadata.create_all(engine)
