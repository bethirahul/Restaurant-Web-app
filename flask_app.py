from flask import Flask, request, redirect
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
def homePage():
    '''Home Page'''
    return html_data.rt_cnt.format(all_res_path=all_res_path)


#========================
# All Restaurants Page
@app.route(all_res_path, methods=['GET'])
def AllRestaurantsPage():
    '''All Restaurants Page'''
    # Get all restaurants
    all_res = session.query(Restaurant)
    if all_res:
        output_html = ''
        for res in all_res:
            output_html += html_data.res_link_cnt.format(
                    res_path = res_path.format(res_id = str(res.id)),
                    res_name = res.name,
                    edit_res_path = edit_res_path.format(res_id = str(res.id)),
                    del_res_path = del_res_path.format(res_id = str(res.id))
                    )
        
        return html_data.all_res_cnt.format(
                add_res_path=add_res_path,
                all_res_cnt=output_html
                )
    
    return redirect(root_path)


#========================
# Add Restaurant Page
@app.route(add_res_path, methods=['GET', 'POST'])
@app.route(add_res_e_path, methods=['GET', 'POST'])
def addRestaurantPage():
    '''Add Restaurant Page'''
    if request.method == 'GET':
        error_html = ''
        if request.path == add_res_e_path:
            error_html = html_data.res_e_cnt
        
        return html_data.add_res_cnt.format(
                all_res_path = all_res_path,
                error = error_html
                )


#========================
# Each Restaurant Page
@app.route(res_path.format(res_id = '<int:res_id>'), methods=['GET'])
def restaurantPage(res_id):
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
                    edit_item_path = edit_item_path.format(
                            res_id = res_id,
                            item_id = item.id
                            ),
                    del_item_path = del_item_path.format(
                            res_id = res_id,
                            item_id = item.id
                            )
                    )

        return html_data.res_cnt.format(
                res_name = res.name,
                all_res_path = all_res_path,
                add_item_path = add_item_path.format(res_id = res.id),
                res_items = output_html
                )
    
    return redirect(all_res_path)


#========================
# Edit Restaurant Page
@app.route(
    edit_res_path.format(res_id = '<int:res_id>'), methods=['GET', 'POST'])
@app.route(
    edit_res_e_path.format(res_id = '<int:res_id>'), methods=['GET', 'POST'])
def editRestaurantPage(res_id):
    '''Edit Restaurant Page'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()

    if request.method == 'GET' and res:
        error_html = ''
        if request.path == edit_res_e_path.format(res_id = res_id):
            error_html = html_data.res_e_cnt
        
        return html_data.edit_res_cnt.format(
                res_name = res.name,
                all_res_path = all_res_path,
                error = error_html
                )
    
    return redirect(all_res_path)


#========================
# Delete Restaurant Page
@app.route(
    del_res_path.format(res_id = '<int:res_id>'), methods=['GET', 'POST'])
def deleteRestaurantPage(res_id):
    '''Delete Restaurant Page'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()

    if request.method == 'GET' and res:
        return html_data.del_res_cnt.format(
                res_name = res.name,
                all_res_path = all_res_path
                )

    return redirect(all_res_path)


#========================
# Add Item Page
@app.route(
    add_item_path.format(res_id = '<int:res_id>'), methods=['GET', 'POST'])
@app.route(
    add_item_e_path.format(res_id = '<int:res_id>'), methods=['GET', 'POST'])
def addItemPage(res_id):
    '''Add Item Page'''
    # Get restaurant
    res = session.query(Restaurant).filter_by(id = res_id).one()

    if request.method == 'GET' and res:
        error_html = ''
        if request.path == add_item_e_path.format(res_id = res_id):
            error_html = html_data.item_e_cnt
        
        return html_data.add_item_cnt.format(
                res_name = res.name,
                res_path = res_path.format(res_id = res_id),
                error = error_html
                )

    return redirect(all_res_path)


#========================
# Edit Item Page
@app.route(
    edit_item_path.format(
        res_id = '<int:res_id>',
        item_id = '<int:item_id>'),
        methods=['GET', 'POST']
        )
@app.route(
    edit_item_e_path.format(
        res_id = '<int:res_id>',
        item_id = '<int:item_id>'),
        methods=['GET', 'POST']
        )
def editItemPage(res_id, item_id):
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
                    res_path = res_path.format(res_id = res_id),
                    item_price = item.price,
                    item_desc = item.description,
                    error = error_html
                    )

    return redirect(all_res_path)


#========================
# Delete Item Page
@app.route(
    del_item_path.format(
        res_id = '<int:res_id>',
        item_id = '<int:item_id>'),
        methods=['GET', 'POST']
        )
def deleteItemPage(res_id, item_id):
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
                    res_path = res_path.format(res_id = res_id)
                )

    return redirect(all_res_path)


if __name__ == '__main__':
    app.debug = True
    app.run(host ='0.0.0.0', port = 8000)