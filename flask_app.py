from flask import Flask, request, redirect, url_for
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
@app.route(root_path, methods=['GET'])
def hmPg():
    '''Home Page'''
    return html_data.rt_cnt.format(all_res_path = url_for('allResPg'))


#========================
# All Restaurants Page
@app.route(all_res_path, methods=['GET'])
def allResPg():
    '''All Restaurants Page'''
    # Get all restaurants
    all_res = session.query(Restaurant)
    if all_res:
        output_html = ''
        for res in all_res:
            output_html += html_data.res_link_cnt.format(
                    res_path = url_for('resPg', res_id = res.id),
                    res_name = res.name,
                    edit_res_path = url_for('editResPath_name', res_id = res.id),
                    del_res_path = url_for('delResPg', res_id = res.id),
                    )
        
        return html_data.all_res_cnt.format(
                add_res_path = url_for('addResPath_name'),
                all_res_cnt = output_html
                )
    
    return redirect(url_for('hmPg'))


#========================
# Add Restaurant Page
@app.route(add_res_path, methods=['GET', 'POST'], endpoint = 'addResPath_name')
@app.route(add_res_e_path, methods=['GET', 'POST'])
def addResPg():
    '''Add Restaurant Page'''
    if request.method == 'GET':
        error_html = ''
        if request.path == add_res_e_path:
            error_html = html_data.res_e_cnt
        
        return html_data.add_res_cnt.format(
                all_res_path = url_for('allResPg'),
                error = error_html
                )


#========================
# Each Restaurant Page
@app.route(res_path.format(res_id = '<int:res_id>'), methods=['GET'])
def resPg(res_id):
    '''Restaurant page with items in it'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()

    if res:
        output_html = ''
        # Get the restaurant's menu items
        items = session.query(MenuItem).filter_by(restaurant_id=res.id)
        for item in items:
            output_html += html_data.res_item_cnt.format(
                    item_name = item.name,
                    item_price = item.price,
                    item_desc = item.description,
                    edit_item_path = url_for(
                            'editItemPath_name',
                            res_id = res_id,
                            item_id = item.id
                            ),
                    del_item_path = url_for(
                            'delItmPg',
                            res_id = res_id,
                            item_id = item.id
                            )
                    )

        return html_data.res_cnt.format(
                res_name = res.name,
                all_res_path = url_for('allResPg'),
                add_item_path = url_for('addItemPath_name', res_id = res.id),
                res_items = output_html
                )
    
    return redirect(url_for('allResPg'))


#========================
# Edit Restaurant Page
@app.route(
    edit_res_path.format(res_id = '<int:res_id>'),
    methods=['GET', 'POST'],
    endpoint = 'editResPath_name'
    )
@app.route(
    edit_res_e_path.format(res_id = '<int:res_id>'), methods=['GET', 'POST'])
def editResPg(res_id):
    '''Edit Restaurant Page'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()

    if request.method == 'GET' and res:
        error_html = ''
        if request.path == edit_res_e_path.format(res_id = res_id):
            error_html = html_data.res_e_cnt
        
        return html_data.edit_res_cnt.format(
                res_name = res.name,
                all_res_path = url_for('allResPg'),
                error = error_html
                )
    
    return redirect(url_for('allResPg'))


#========================
# Delete Restaurant Page
@app.route(
    del_res_path.format(res_id = '<int:res_id>'), methods=['GET', 'POST'])
def delResPg(res_id):
    '''Delete Restaurant Page'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()

    if request.method == 'GET' and res:
        return html_data.del_res_cnt.format(
                res_name = res.name,
                all_res_path = url_for('allResPg')
                )

    return redirect(url_for('allResPg'))


#========================
# Add Item Page
@app.route(
    add_item_path.format(res_id = '<int:res_id>'),
    methods=['GET', 'POST'],
    endpoint = 'addItemPath_name'
    )
@app.route(
    add_item_e_path.format(res_id = '<int:res_id>'), methods=['GET', 'POST'])
def addItmPg(res_id):
    '''Add Item Page'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()

    if request.method == 'GET' and res:
        error_html = ''
        if request.path == add_item_e_path.format(res_id = res_id):
            error_html = html_data.item_e_cnt
        
        return html_data.add_item_cnt.format(
                res_name = res.name,
                res_path = url_for('resPg', res_id = res_id),
                error = error_html
                )

    return redirect(url_for('allResPg'))


#========================
# Edit Item Page
@app.route(
    edit_item_path.format(
        res_id = '<int:res_id>',
        item_id = '<int:item_id>'),
        methods=['GET', 'POST'],
        endpoint = 'editItemPath_name'
        )
@app.route(
    edit_item_e_path.format(
        res_id = '<int:res_id>',
        item_id = '<int:item_id>'),
        methods=['GET', 'POST']
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
            error_html = ''
            if request.path == edit_item_e_path.format(
                    res_id = res_id,
                    item_id = item_id
                ):
                error_html = html_data.item_e_cnt
            
            return html_data.edit_item_cnt.format(
                    item_name = item.name,
                    res_name = res.name,
                    res_path = url_for('resPg', res_id = res_id),
                    item_price = item.price,
                    item_desc = item.description,
                    error = error_html
                    )

    return redirect(url_for('allResPg'))


#========================
# Delete Item Page
@app.route(
    del_item_path.format(
        res_id = '<int:res_id>',
        item_id = '<int:item_id>'),
        methods=['GET', 'POST']
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
            return html_data.del_item_cnt.format(
                    item_name = item.name,
                    res_name = res.name,
                    res_path = url_for('resPg', res_id = res_id)
                )

    return redirect(url_for('allResPg'))


if __name__ == '__main__':
    app.debug = True
    app.run(host ='0.0.0.0', port = 8000)