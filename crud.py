#!/usr/bin/env python3

# Functions and variables used to manipulate different parts of python runtime environment
import sys

# SQLAlchemy variables used in writing mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# To use in configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# To relate Foreign Key relationships
from sqlalchemy.orm import relationship

# To use in the configuration code at the end of configuration
from sqlalchemy import create_engine

# Basic HTTP server
from http.server import HTTPServer, BaseHTTPRequestHandler

# Tools for parsing the incoming messages from clients
from urllib.parse import parse_qs

# Tools for threading, used to recieve and handle multiple requests at once
import threading
from socketserver import ThreadingMixIn


# Instance of the declarative base class
Base = declarative_base()
# ^^Will let the SQLAlchemy know that out classes are special SQLAlchemy classes that correspond to the tables in our database


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class MessageHandler(BaseHTTPRequestHandler):
    """To handle messages from the client"""
    def do_GET(self):
        # First send a 200 OK response
        self.send_response(200)

        # Then send headers

    def do_POST(self):



if __name__ == '__main__':
    port = 8080
    address = ('', port)
    my_server = ThreadedHTTPServer(address, MessageHandler)
    print("Server is up and running! >>>>>>>>>>")
    my_server.serve_forever()


    








########## At End of File ##########

# Instance of create engine class and point to database we use
## engine = create_engine('sqlite:///restaurants.db')
# ^^Above example has SQLite3 with database 'restaurant'

# This goes into database and creates all the classes we will soon create as new tables
## Base.metadata.create_all(engine)