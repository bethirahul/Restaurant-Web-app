from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import html_data


# First set Flask app
app = Flask(__name__)

# Setting database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

root_path = '/'
all_res_path = '/restaurants/'
add_res_path = '/restaurants/add/'


# These must be placed after setting database and Flask name to flask app
@app.route('/')
def helloWorld():
    output_text = '<a href=/restaurants/>Show all restaurants</a>'
    return output_text

@app.route('/restaurants/')
def showAllRestaurants():
    # Get all restaurants
    restaurants = session.query(Restaurant)
    for res in restaurants:
        output_text += '<br><br><a href=/restaurants/' + str(res.id) + '/>' + res.name + '</a>'
    
    return html_data.res_cnt.format('/restaurants/add/')

@app.route('/restaurants/add/')
def addRestaurant():
    # Add new restaurant
    res = Restaurant

@app.route('/restaurants/<int:res_id>/')
def restaurantMenu(res_id):
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()
    output_text = res.name + '<br><br>'

    # Get the restaurant's menu items
    items = session.query(MenuItem).filter_by(restaurant_id=res.id)
    for item in items:
        output_text += item.name + '<br>'
        output_text += item.price + '<br>'
        output_text += item.description + '<br>'
        output_text += '<br>'

    return output_text




if __name__ == '__main__':
    app.debug = True
    app.run(host ='0.0.0.0', port = 8000)