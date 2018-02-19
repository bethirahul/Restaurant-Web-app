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
add_res_path = all_res_path + 'add/' ##
add_res_e_path = add_res_path + 'error/' ##
### Needs Restaurant ID
res_path = all_res_path + '{res_id}/' ##
edit_res_path = res_path + 'edit/' ##
edit_res_e_path = edit_res_path + 'error/' ##
del_res_path = res_path + 'delete/' ##
add_item_path = res_path + 'add/' ##
add_item_e_path = add_item_path + 'error/' ##
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

    # Found Restaurants table
    if all_res:
        return render_template('all_res.html', all_res = all_res)
    
    # Cannot find Restaurants table
    return redirect(url_for('index'))


#========================
# Add Restaurant Page
@app.route(
    add_res_path,
    methods = ['GET', 'POST'],
    endpoint = 'addResPath_name'
)
@app.route(
    add_res_e_path,
    methods = ['GET', 'POST'],
    endpoint = 'addResErrorPath_name'
)
def addResPg():
    '''Add Restaurant Page'''
    # GET
    if request.method == 'GET':
        error = False
        if request.path == add_res_e_path:
            error = True
        
        return render_template('add_res.html', error = error)
    
    # POST
    # Input empty
    if request.form['res_name'] == '':
        return redirect(url_for('addResErrorPath_name'))

    # Input not empty
    new_res = Restaurant(name = request.form['res_name'])
    session.add(new_res)
    session.commit()

    return redirect(url_for('allResPg'))
        

#========================
# Each Restaurant Page
@app.route(res_path.format(res_id = '<int:res_id>'), methods = ['GET'])
def resPg(res_id):
    '''Restaurant page with items in it'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()

    # Found restaurant
    if res:
        # Get the restaurant's menu items
        items = session.query(MenuItem).filter_by(restaurant_id = res.id)
        
        return render_template('res.html', res = res, items = items)
    
    # Cannot find Restaurant
    return redirect(url_for('allResPg'))


#========================
# Edit Restaurant Page
@app.route(
    edit_res_path.format(res_id = '<int:res_id>'),
    methods = ['GET', 'POST'],
    endpoint = 'editResPath_name'
)
@app.route(
    edit_res_e_path.format(res_id = '<int:res_id>'),
    methods = ['GET', 'POST'],
    endpoint = 'editResErrorPath_name'
)
def editResPg(res_id):
    '''Edit Restaurant Page'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()

    # Found restaurant
    if res:

        # GET
        if request.method == 'GET':
            error = False
            if request.path == edit_res_e_path.format(res_id = res_id):
                error = True
            
            return render_template(
                    'edit_res.html',
                    res_name = res.name,
                    error = error
                )
        
        # POST
        # Input empty
        if request.form['res_name'] == '':
            return redirect(url_for('editResErrorPath_name', res_id = res_id))

        # Input not empty
        if request.form['res_name'] != res.name:
            res.name = request.form['res_name']
            session.commit()

    # After adding Restaurant OR
    # Cannot find Restaurant
    return redirect(url_for('allResPg'))


#========================
# Delete Restaurant Page
@app.route(
    del_res_path.format(res_id = '<int:res_id>'), methods = ['GET', 'POST'])
def delResPg(res_id):
    '''Delete Restaurant Page'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()

    # Found Restaurant
    if res:

        # GET
        if request.method == 'GET':
            return render_template('del_res.html', res_name = res.name)
        
        # POST
        session.delete(res)
        session.commit()

    # After deleting Restaurant OR
    # Cannot find Restaurant
    return redirect(url_for('allResPg'))


#========================
# Add Item Page
@app.route(
    add_item_path.format(res_id = '<int:res_id>'),
    methods = ['GET', 'POST'],
    endpoint = 'addItemPath_name'
)
@app.route(
    add_item_e_path.format(res_id = '<int:res_id>'),
    methods = ['GET', 'POST'],
    endpoint = 'addItemErrorPath_name'
)
def addItmPg(res_id):
    '''Add Item Page'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()

    # Found Restaurant
    if res:
        
        # GET
        if request.method == 'GET':
            error = False
            if request.path == add_item_e_path.format(res_id = res_id):
                error = True
            
            return render_template('add_item.html', res = res, error = error)
        
        # POST
        # Input name empty
        if request.form['item_name'] == '':
            return redirect(url_for('addItemErrorPath_name', res_id = res_id))

        # Input name not empty
        new_item = MenuItem(
                name = request.form['item_name'],
                price = request.form['item_price'],
                description = request.form['item_desc'],
                restaurant_id = res_id
            )
        session.add(new_item)
        session.commit()

        return redirect(url_for('resPg', res_id = res_id))

    # Cannot find Restaurant
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
    methods = ['GET', 'POST'],
    endpoint = 'editItemErrorPath_name'
)
def editItmPg(res_id, item_id):
    '''Edit Item Page'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()

    # Found Restaurant
    if res:

        # Get item
        item = session.query(MenuItem).filter_by(
                id = item_id,
                restaurant_id = res_id
            ).one()

        # Found Item
        if item:

            # GET
            if request.method == 'GET':
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
            
            # POST
            # Input name empty
            if request.form['item_name'] == '':
                return redirect(
                        url_for(
                            'editItemErrorPath_name',
                            res_id = res_id,
                            item_id = item_id
                        )
                    )

            # Input name not empty
            if  (
                    item.name != request.form['item_name'] or
                    item.price != request.form['item_price'] or
                    item.description != request.form['item_desc']
                ):
                if item.name != request.form['item_name']:
                    item.name = request.form['item_name']
                if item.price != request.form['item_price']:
                    item.price = request.form['item_price']
                if item.description != request.form['item_desc']:
                    item.description = request.form['item_desc']
                session.commit()
        
        # After editing Item OR
        # Cannot find Item
        return redirect(url_for('resPg', res_id = res_id))

    # Cannot find Restaurant
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

    # Found Restaurant
    if res:

        # Get item
        item = session.query(MenuItem).filter_by(
                id = item_id,
                restaurant_id = res_id
            ).one()

        # Found Item
        if item:

            # GET
            if request.method == 'GET':
                return render_template(
                        'del_item.html',
                        item_name = item.name,
                        res = res,
                    )
            
            # POST
            session.delete(item)
            session.commit()

        # After deleting Restaurant OR
        # Cannot find item
        return redirect(url_for('resPg', res_id = res_id))

    # Cannot find Restaurant
    return redirect(url_for('allResPg'))


if __name__ == '__main__':
    app.debug = True
    app.run(host ='0.0.0.0', port = 8000)