from flask import Flask, request, redirect, url_for, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import html_data


# First set Flask app
app = Flask(__name__)

# Setting database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# Home Page
root_path = '/' ##
## Restaurants
all_res_path = root_path + 'restaurants/' ##
add_res_path = all_res_path + 'add/' #
add_res_e_path = add_res_path + 'error/' #
### Needs Restaurant ID
res_path = all_res_path + '{res_id}/' ##
edit_res_path = res_path + 'edit/' #
edit_res_e_path = edit_res_path + 'error/' #
del_res_path = res_path + 'delete/' #
add_item_path = res_path + 'add/' #
add_item_e_path = add_item_path + 'error/' #
#### Needs Restaurant ID and Item ID
edit_item_path = res_path + '{item_id}-edit/' #
edit_item_e_path = edit_item_path + 'error/' #
del_item_path = res_path + '{item_id}-delete/' #


# These must be placed after setting database and Flask name to flask app

#========================
# Root - Home Page
@app.route(root_path, methods = ['GET'])
def index():
    '''Home Page'''
    return render_template('index.html')


#========================
# All Restaurants Page
@app.route(all_res_path, methods = ['GET'])
def allResPg():
    '''All Restaurants Page'''
    # Get all restaurants
    all_res = session.query(Restaurant)
    if all_res:
        return render_template('all_res.html', all_res = all_res)
    
    return redirect(url_for('index'))


#========================
# Add Restaurant Page
@app.route(
    add_res_path,
    methods = ['GET', 'POST'],
    endpoint = 'addResPath_name'
)
@app.route(add_res_e_path, methods = ['GET', 'POST'])
def addResPg():
    '''Add Restaurant Page'''
    if request.method == 'GET':
        error = False
        if request.path == add_res_e_path:
            error = True
        
        return render_template('add_res.html', error = error)
        

#========================
# Each Restaurant Page
@app.route(res_path.format(res_id = '<int:res_id>'), methods = ['GET'])
def resPg(res_id):
    '''Restaurant page with items in it'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()

    if res:
        # Get the restaurant's menu items
        items = session.query(MenuItem).filter_by(restaurant_id = res.id)
        
        return render_template('res.html', res = res, items = items)
    
    return redirect(url_for('allResPg'))


#========================
# Edit Restaurant Page
@app.route(
    edit_res_path.format(res_id = '<int:res_id>'),
    methods = ['GET', 'POST'],
    endpoint = 'editResPath_name'
)
@app.route(
    edit_res_e_path.format(res_id = '<int:res_id>'), methods = ['GET', 'POST'])
def editResPg(res_id):
    '''Edit Restaurant Page'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()

    if request.method == 'GET' and res:
        error = False
        if request.path == edit_res_e_path.format(res_id = res_id):
            error = True
        
        return render_template(
                'edit_res.html',
                res_name = res.name,
                error = error
            )
    
    return redirect(url_for('allResPg'))


#========================
# Delete Restaurant Page
@app.route(
    del_res_path.format(res_id = '<int:res_id>'), methods = ['GET', 'POST'])
def delResPg(res_id):
    '''Delete Restaurant Page'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()

    if request.method == 'GET' and res:
        return render_template('del_res.html', res_name = res.name)

    return redirect(url_for('allResPg'))


#========================
# Add Item Page
@app.route(
    add_item_path.format(res_id = '<int:res_id>'),
    methods = ['GET', 'POST'],
    endpoint = 'addItemPath_name'
)
@app.route(
    add_item_e_path.format(res_id = '<int:res_id>'), methods = ['GET', 'POST'])
def addItmPg(res_id):
    '''Add Item Page'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()

    if request.method == 'GET' and res:
        error = False
        if request.path == add_item_e_path.format(res_id = res_id):
            error = True
        
        return render_template('add_item.html', res = res, error = error)

    return redirect(url_for('allResPg'))


#========================
# Edit Item Page
@app.route(
    edit_item_path.format(res_id = '<int:res_id>', item_id = '<int:item_id>'),
    methods = ['GET', 'POST'],
    endpoint = 'editItemPath_name'
)
@app.route(
    edit_item_e_path.format(res_id = '<int:res_id>', item_id = '<int:item_id>'),
    methods = ['GET', 'POST']
)
def editItmPg(res_id, item_id):
    '''Edit Item Page'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()
    if res:
        item = session.query(MenuItem).filter_by(
                id = item_id,
                restaurant_id = res_id
            ).one()

        if request.method == 'GET' and item:
            error = False
            if request.path == edit_item_e_path.format(
                    res_id = res_id,
                    item_id = item_id
                ):
                error = True
            
            return render_template(
                    'edit_item.html',
                    item = item,
                    res = res,
                    error = error
                )

    return redirect(url_for('allResPg'))


#========================
# Delete Item Page
@app.route(
    del_item_path.format(res_id = '<int:res_id>', item_id = '<int:item_id>'),
    methods = ['GET', 'POST']
    )
def delItmPg(res_id, item_id):
    '''Delete Item Page'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()
    if res:
        item = session.query(MenuItem).filter_by(
                id = item_id,
                restaurant_id = res_id
            ).one()

        if request.method == 'GET' and item:
            return render_template(
                    'del_item.html',
                    item_name = item.name,
                    res = res,
                )

    return redirect(url_for('allResPg'))


if __name__ == '__main__':
    app.debug = True
    app.run(host ='0.0.0.0', port = 8000)