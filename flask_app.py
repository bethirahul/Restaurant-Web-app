from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


# First set Flask app
app = Flask(__name__)

# Setting database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# These must be placed after setting database and Flask name to flask app
@app.route('/')
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