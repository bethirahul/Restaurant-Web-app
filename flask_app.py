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
all_res_path = root_path + 'restaurants/'
add_res_path = all_res_path + 'add/'
res_path = all_res_path + '{}/'
edit_res_path = res_path + 'edit/'
del_res_path = res_path + 'delete/'


# These must be placed after setting database and Flask name to flask app
@app.route(root_path)
def homePage():
    return html_data.rt_cnt.format(all_res_path=all_res_path)

@app.route(all_res_path)
def showAllRestaurants():
    # Get all restaurants
    all_res = session.query(Restaurant)
    if all_res:
        output_html = ''
        for res in all_res:
            output_html += html_data.res_cnt.format(
                    res_path = res_path.format(str(res.id)),
                    res_name = res.name,
                    edit_res_path = edit_res_path.format(str(res.id)),
                    del_res_path = del_res_path.format(str(res.id))
                )
        
        return html_data.res_cnt.format(
                add_res_path=add_res_path,
                all_res_cnt=output_html
            )
    
    return 'SQL Error: Unable to fetch restaurants!'

@app.route(add_res_path)
def addRestaurant():
    # Add new restaurant
    res = Restaurant

@app.route(res_path.format('<int:res_id>'))
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