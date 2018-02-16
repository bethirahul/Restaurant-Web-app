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


# Instance of the declarative base class
Base = declarative_base()
# ^^ Will let the SQLAlchemy know that out classes are special SQLAlchemy
#   classes that correspond to the tables in our database


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
