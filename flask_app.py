# To use Flask framework
from flask import Flask, request, redirect
# To use decorators as links to pages
from flask import url_for
# To use HTML templates
from flask import render_template
# To send flash messages
from flask import flash
# To send JSON format messages
from flask import jsonify
# To use 3rd-party OAuth 2 providers
from flask import session

# To generate random string to stop hacking session
import random
import string

# To use SQLAlchemy
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

# To use the tables classes we setup in our database
from database_setup import Base, Restaurant, MenuItem, User

# To use OAuth 2
# This creates a flow object from client secretes JSON file
#   client ID, client secret, etc. OAuth 2 parameters
from oauth2client.client import flow_from_clientsecrets
# To catch error when trying to exchange authorization code for an access token
from oauth2client.client import FlowExchangeError
# Python's comprehensive HTTP client Library
import httplib2
# API to convert Python objects to JSON format
import json
# Flask module to convert a function's returned value into a real response obj
# to send to the client
from flask import make_response
# Apache 2.0 licensed HTTP library (different from flask >> request)
# similar to urllib2 but with improvements
import requests


# First set Flask app
app = Flask(__name__)

# Setting database
engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# Home Page
root_path = '/'
login_path = '/login'
g_login_success_path = '/gconnect'
fb_login_success_path = '/fbconnect'
g_logout_path = '/gdisconnect'
fb_logout_path = '/fbdisconnect'
# -> Restaurants
all_res_path = root_path + 'restaurants/'
add_res_path = all_res_path + 'add/'
json_all_res_path = all_res_path + 'json/'
# ->-> Needs Restaurant ID
res_path = all_res_path + '{res_id}/'
edit_res_path = res_path + 'edit/'
del_res_path = res_path + 'delete/'
add_item_path = res_path + 'add/'
json_res_path = res_path + 'json/'
# ->->-> Needs Restaurant ID and Item ID
item_path = res_path + '{item_id}/'
json_item_path = item_path + 'json/'
edit_item_path = item_path + 'edit/'
del_item_path = item_path + 'delete/'

# Get (JSON Decoding) client ID from the json file which is downloaded from
# the Google OAuth2 developer website for this app
CLIENT_ID = json.loads(
        open('client_secrets.json', 'r').read()
    )['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"


# These must be placed after setting database and Flask name to flask app

# ========================
# Root - Home Page
@app.route(root_path, methods=['GET'])
def index():
    '''Home Page'''

    logged_in = False
    if 'username' in session:
        user_id = getUserID()
        logged_in = True

    return render_template('index.html', logged_in=logged_in)


# ========================
# Login Page
@app.route(login_path, methods=['GET'])
def loginPg():
    '''Login Page'''

    # Get previous website path to redirect back
    if request.referrer is None:
        prev_path = ''
    else:
        prev_path = request.referrer
    print("\nLogin Page's - Previous Page: " + prev_path)

    # Generate Random token
    state_token = ''
    for i in range(0, 32):
        state_token += random.choice(string.ascii_letters + string.digits)
    # ^^Can also be written as
    # state_token = ''.join(
    #       random.choice(
    #           string.ascii_letters + string.digits
    #       ) for x in xrange(32)
    #   )
    # Send the state_token to session by assigning it to
    # session's state argument
    session['state'] = state_token
    return render_template(
            'login.html',
            STATE=state_token,
            prev_path=prev_path
        )


# Google Login Success Response - POST
@app.route(g_login_success_path, methods=['POST'])
def gconnect():
    '''Google Sign-in response handler'''
    # If session's argument state (state_token) doesn't match with the
    # response's state argument, return error 401.
    # Round-trip verification
    # [To stop Cross-site Reference Forgery attacks]
    if request.args.get('state') != session['state']:
        # Make and send error response 401 with a message by encoding with JSON
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'

        return response  # 401

    # If the state_tokens matched
    # Collect one-time-use code from the Google server
    code = request.data

    # Trying to use one-time-use code to exchange it with credentials object
    # which contains the access token for the server
    try:
        # Create new OAuth Flow object with Client's Secrete key info
        # from 'clients_screte.json' file
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        # Message type -> POST
        oauth_flow.redirect_uri = 'postmessage'
        # Get credentials object by initiating setp2 exchange with the
        # one-time-use code as input
        credentials = oauth_flow.step2_exchange(code)

    # If error occurs in ^^above (step2 exchange)
    except FlowExchangeError:
        # Make and send error response 401 with a message by encoding with JSON
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'

        return response  # 401

    # If credentials is obtained without Flow error,
    # check if the access token is valid

    # Get Access token from the obtained Credentials object
    access_token = credentials.access_token
    # Google API URL to validate the Access Token
    url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'.format(access_token)
    # Perform JSON decode on HTTP GET request response of the url
    # to get the validation result
    result = json.loads(httplib2.Http().request(url, 'GET')[1].decode())

    # Check for errors in result
    if result.get('error') is not None:
        # Make and send error response 500 Internal Server Error with the error
        # message from result by encoding with JSON
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

        return response  # 500

    # If no errors, then Access token is available without errors,
    # but check for the right Access token

    # Get Google ID from credentials
    gplus_id = credentials.id_token['sub']

    # If Access Token's User ID is not the same as Google ID from credentials
    if result['user_id'] != gplus_id:
        # Make and send error response 401 with a message by encoding with JSON
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'

        return response  # 401

    # Check if Access Token is issued for this app by checking with CLIENT ID
    if result['issued_to'] != CLIENT_ID:
        # Make and send error response 401 with a message by encoding with JSON
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'

        return response  # 401

    # Check if User is already Logged-in
    stored_access_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        # Updating access token with the latest one
        session['access_token'] = credentials.access_token
        # Make and send a 200 OK response with a message by encoding with JSON
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'

        return response  # 200

    # If the User is not Logged-in before, store the credentials and Google ID
    # to check for Logged-in next time - to avoid Logging-in again
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get Google User Info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    userinfo_parameters = {
            'access_token': credentials.access_token,
            'alt': 'json'
        }
    # Send and get response from that URL
    userinfo_response = requests.get(userinfo_url, params=userinfo_parameters)
    userinfo = userinfo_response.json()

    session['provider'] = 'google'
    session['username'] = userinfo['name']
    session['picture'] = userinfo['picture']  # picture URL
    session['email'] = userinfo['email']

    # Check if user is already exists
    user_id = getUserID()
    if user_id is None:
        createUser()
        print("New User Created!")
    
    print('\nUser Table:')
    users = db_session.query(User).all()
    for user in users:
        print(str(user.id) + ": " + user.name + ": " + user.email)

    #flash("you are now logged in as {}".format(session['username']))

    print("done!")

    output = '''<h1>Welcome, {name}!</h1>
    <img
      src="{pic_url}"
      style = "
        width: 300px;
        height: 300px;
        border-radius: 150px;
        -webkit-border-radius: 150px;
        -moz-border-radius: 150px;">
    '''
    return output.format(
            name=session['username'],
            pic_url=session['picture']
        )


# Facebook Login success Response - POST
@app.route(fb_login_success_path, method=['POST'])
def fbconnect():
    '''Facebook Sign-in Response handler'''
    # If session's argument state (state_token) doesn't match with the
    # response's state argument, return error 401.
    # Round-trip verification
    # [To stop Cross-site Reference Forgery attacks]
    if request.args.get('state') != session['state']:
        # Make and send error response 401 with a message by encoding with JSON
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'

        return response  # 401
    
    # If the state_tokens matched
    # Collect access_token (short_lived) from the Facebook server
    # Similar to one-time-use code of Google
    access_token = request.data

    # Trying to use access_token (short_lived) to exchange it with
    # acess_token (long-lived)
    app_id = json.loads(
            open('fb_client_secrets.json', 'r').read()
        )['web']['app_id']
    app_secret = json.loads(
            open('fb_client_secrets.json', 'r').read()
        )['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={app_id}$client_secret={app_secret}&fb_secret_token={access_token}'.format(
            app_id=app_id,
            app_secret=app_secret,
            access_token=access_token
        )
    result = httplib2.Http().request(url, 'GET')[1]

    # **Check result error is not done here

    # Get the access_token (long lived) from the response
    # Response has few fileds
    #   - Token & Expiration (UNIX time) & signedRequest & userID
    # Expiration can last upto 2 months
    access_token = result.split("&")[0]
    session['access_token'] = access_token
    session['id'] = 

    # Use token to get user information
    userinfo_url = 'https://graph.facebook.com/v2.8/me?access_token={}&fields=name,id,email'.format(token)
    userinfo_response = httplib2.Http().request(userinfo_url, 'GET')[1]

    # Decode the response using JSON to get the user information
    userinfo = json.loads(userinfo_response)
    session['provider'] = 'facebook'
    session['username'] = userinfo['name']
    session['facebook_id'] = userinfo['id']
    session['email'] = userinfo['email']

    # Facebook uses different API to get Profile picture
    picture_url = 'https://graph.facebook.com/v2.2/me/picture?{}&redirect=0&height=200&width=200'.format(token)
    picture_response = httplib2.Http().request(picture_url, 'GET')[1]

    # Decode the response using JSON to get the picture url
    picture_info = json.loads(picture_response)
    session['picture'] = picture_info['data']['url']

    # Check if user is already exists
    user_id = getUserID()
    if user_id is None:
        createUser()
        print("New User Created!")

    print('\nUser Table:')
    users = db_session.query(User).all()
    for user in users:
        print(str(user.id) + ": " + user.name + ": " + user.email)

    #flash("you are now logged in as {}".format(session['username']))

    print("done!")

    output = '''<h1>Welcome, {name}!</h1>
    <img
      src="{pic_url}"
      style = "
        width: 300px;
        height: 300px;
        border-radius: 150px;
        -webkit-border-radius: 150px;
        -moz-border-radius: 150px;">
    '''
    return output.format(
            name=session['username'],
            pic_url=session['picture']
        )


# ========================
# Google Logout Page
@app.route(g_logout_path, methods=['GET'])
def gdisconnectPg():
    '''Logout Page'''

    # Get previous website path to redirect back
    if request.referrer is None:
        prev_path = ''
    else:
        prev_path = request.referrer
    print("\nLogin Page's - Previous Page: " + prev_path)

    # To only disconnect a connected user, check Access Token
    access_token = session.get('access_token')

    # If Access Token is None, then the user is not connected before
    if access_token is None:
        print('Access Token is None')
        # Make and send error response 401 with a message by encoding with JSON
        response = make_response(
                json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'

        return response  # 401

    # If Access Token is Available
    print('\n>> In gdisconnect access token is:\n' + access_token)
    print('>> User name is: ' + session['username'])
    print('>> Connected through: ' + session['provider'])

    # Check if connected through google, get Google URL
    if session['provider'] == 'google':
        # Send the Access Token to Google to revoke access to that token
        url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(
            session['access_token'])
    # Or else Facebook URL
    else:
        url = 'https://graph.facebook.com/{}/permissions'.format(
                session['facebook_id'])
    # Disconnect and get the response
    result = httplib2.Http().request(url, 'GET')[0]

    # Check if the response is 200 OK
    if result['status'] == '200':
        # Delete all the session variables used for that user
        if session['provider'] == 'facebook':
            del session['facebook_id']

        del session['provider']
        del session['access_token']
        del session['gplus_id']
        del session['username']
        del session['email']
        del session['picture']
        # Make and send a 200 OK response with a message by encoding with JSON
        # response = make_response(json.dumps('Successfully disconnected.'), 200)
        # response.headers['Content-Type'] = 'application/json'

        # return response  # 200

        return render_template('logout.html', prev_path=prev_path)

    # If the response from google was NOT 200 OK
    # Make and send error response 400 with a message by encoding with JSON
    response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
    response.headers['Content-Type'] = 'application/json'

    return response  # 400


# ========================
# All Restaurants Page
@app.route(all_res_path, methods=['GET'])
def allResPg():
    '''All Restaurants Page'''
    # Get all restaurants
    all_res = db_session.query(Restaurant)

    # Found Restaurants table
    if all_res:
        user_id = 0
        logged_in = False
        if 'username' in session:
            user_id = getUserID()
            logged_in = True

        return render_template(
                'all_res.html',
                logged_in=logged_in,
                all_res=all_res,
                user_id=user_id
            )

    # Cannot find Restaurants table
    return redirect(url_for('index'))


# ========================
# All Restaurants (JSON)
@app.route(json_all_res_path, methods=['GET'])
def allResJSON():
    '''All Restaurants in JSON'''
    # Get all restaurants
    all_res = db_session.query(Restaurant)

    # Found Restaurants table
    if all_res:
        return jsonify(Restaurants=[res.serialize for res in all_res])


# ========================
# Add Restaurant Page
@app.route(add_res_path, methods=['GET', 'POST'])
def addResPg():
    '''Add Restaurant Page'''
    # Check if Logged in
    if 'username' not in session:
        return redirect(url_for('loginPg'))

    # GET
    if request.method == 'GET':
        return render_template('add_res.html')

    # POST
    # Input empty
    if request.form['res_name'] == '':
        flash('Error: Please fill in the Restaurant name!')
        return redirect(url_for('addResPg'))

    # Input not empty
    user_id = getUserID()
    new_res = Restaurant(name=request.form['res_name'], creater_id=user_id)
    db_session.add(new_res)
    db_session.commit()
    
    return redirect(url_for('allResPg'))


# ========================
# Each Restaurant Page
@app.route(res_path.format(res_id='<int:res_id>'), methods=['GET'])
def resPg(res_id):
    '''Restaurant page with items in it'''
    # Get restaurant
    res = db_session.query(Restaurant).filter_by(id=res_id).one()

    # Found restaurant
    if res:
        # Get creater for creater name
        creater = getUser(res.creater_id)

        # Found creater
        if creater:
            # Get the restaurant's menu items
            items = db_session.query(MenuItem).filter_by(restaurant_id=res.id)

            # Get user id
            user_id = 0
            logged_in = False
            if 'username' in session:
                user_id = getUserID()
                logged_in = True

            return render_template(
                    'res.html',
                    res=res,
                    logged_in=logged_in,
                    creater_name=creater.name,
                    user_id = user_id,
                    items=items
                )

    # Cannot find Restaurant
    return redirect(url_for('allResPg'))


# ========================
# Each Restaurant (JSON)
@app.route(json_res_path.format(res_id='<int:res_id>'), methods=['GET'])
def resJSON(res_id):
    '''Each Restaurant Page'''

    # Get Restaurant
    res = db_session.query(Restaurant).filter_by(id=res_id).one()

    # Found restaurant
    if res:
        # Get Items
        items = db_session.query(MenuItem).filter_by(
                restaurant_id=res_id).all()

        # Return in JSON format
        return jsonify(MenuItems=[item.serialize for item in items])


# ========================
# Edit Restaurant Page
@app.route(
    edit_res_path.format(res_id='<int:res_id>'),
    methods=['GET', 'POST']
)
def editResPg(res_id):
    '''Edit Restaurant Page'''
    # Check if Logged in
    if 'username' not in session:
        return redirect(url_for('loginPg'))

    # Get restaurant
    res = db_session.query(Restaurant).filter_by(id=res_id).one()

    # Found restaurant
    if res:

        # GET
        if request.method == 'GET':
            return render_template(
                    'edit_res.html',
                    res_name=res.name
                )

        # POST
        # Input empty
        if request.form['res_name'] == '':
            flash('Error: Restaurant name cannot be empty!')
            return redirect(url_for('editResPg', res_id=res_id))

        # Input not empty
        if request.form['res_name'] != res.name:
            res.name = request.form['res_name']
            db_session.commit()

    # After adding Restaurant OR
    # Cannot find Restaurant
    return redirect(url_for('allResPg'))


# ========================
# Delete Restaurant Page
@app.route(
    del_res_path.format(res_id='<int:res_id>'), methods=['GET', 'POST'])
def delResPg(res_id):
    '''Delete Restaurant Page'''
    # Check if Logged in
    if 'username' not in session:
        return redirect(url_for('loginPg'))

    # Get restaurant
    res = db_session.query(Restaurant).filter_by(id=res_id).one()

    # Found Restaurant
    if res:

        # GET
        if request.method == 'GET':
            return render_template('del_res.html', res_name=res.name)

        # POST
        # First delete the items of the restaurant
        items = db_session.query(MenuItem).filter_by(restaurant_id=res_id)
        for item in items:
            db_session.delete(item)
        # Next delete the restaurant
        db_session.delete(res)
        db_session.commit()

    # After deleting Restaurant OR
    # Cannot find Restaurant
    return redirect(url_for('allResPg'))


# ========================
# Add Item Page
@app.route(
    add_item_path.format(res_id='<int:res_id>'),
    methods=['GET', 'POST']
)
def addItmPg(res_id):
    '''Add Item Page'''
    # Check if Logged in
    if 'username' not in session:
        return redirect(url_for('loginPg'))

    # Get restaurant
    res = db_session.query(Restaurant).filter_by(id=res_id).one()

    # Found Restaurant
    if res:

        # GET
        if request.method == 'GET':
            return render_template('add_item.html', res=res)

        # POST
        # Input name empty
        if request.form['item_name'] == '':
            flash('Error: Please fill in the Item name!')
            return redirect(url_for('addItmPg', res_id=res_id))

        # Input name not empty
        new_item = MenuItem(
                name=request.form['item_name'],
                price=request.form['item_price'],
                description=request.form['item_desc'],
                restaurant_id=res_id
            )
        db_session.add(new_item)
        db_session.commit()

        return redirect(url_for('resPg', res_id=res_id))

    # Cannot find Restaurant
    return redirect(url_for('allResPg'))


# ========================
# Edit Item Page
@app.route(
    edit_item_path.format(res_id='<int:res_id>', item_id='<int:item_id>'),
    methods=['GET', 'POST']
)
def editItmPg(res_id, item_id):
    '''Edit Item Page'''
    # Check if Logged in
    if 'username' not in session:
        return redirect(url_for('loginPg'))

    # Get restaurant
    res = db_session.query(Restaurant).filter_by(id=res_id).one()

    # Found Restaurant
    if res:

        # Get item
        item = db_session.query(MenuItem).filter_by(
                id=item_id,
                restaurant_id=res_id
            ).one()

        # Found Item
        if item:

            # GET
            if request.method == 'GET':
                return render_template(
                        'edit_item.html',
                        item=item,
                        res=res
                    )

            # POST
            # Input name empty
            if request.form['item_name'] == '':
                flash('Error: Item name cannot be empty!')
                return redirect(
                        url_for(
                            'editItmPg',
                            res_id=res_id,
                            item_id=item_id
                        )
                    )

            # Input name not empty
            if (item.name != request.form['item_name'] or
                    item.price != request.form['item_price'] or
                    item.description != request.form['item_desc']):
                if item.name != request.form['item_name']:
                    item.name = request.form['item_name']
                if item.price != request.form['item_price']:
                    item.price = request.form['item_price']
                if item.description != request.form['item_desc']:
                    item.description = request.form['item_desc']
                db_session.commit()

        # After editing Item OR
        # Cannot find Item
        return redirect(url_for('resPg', res_id=res_id))

    # Cannot find Restaurant
    return redirect(url_for('allResPg'))


# ========================
# Delete Item Page
@app.route(
    del_item_path.format(res_id='<int:res_id>', item_id='<int:item_id>'),
    methods=['GET', 'POST']
    )
def delItmPg(res_id, item_id):
    '''Delete Item Page'''
    # Check if Logged in
    if 'username' not in session:
        return redirect(url_for('loginPg'))

    # Get restaurant
    res = db_session.query(Restaurant).filter_by(id=res_id).one()

    # Found Restaurant
    if res:

        # Get item
        item = db_session.query(MenuItem).filter_by(
                id=item_id,
                restaurant_id=res_id
            ).one()

        # Found Item
        if item:

            # GET
            if request.method == 'GET':
                return render_template(
                        'del_item.html',
                        item_name=item.name,
                        res=res,
                    )

            # POST
            db_session.delete(item)
            db_session.commit()

        # After deleting Restaurant OR
        # Cannot find item
        return redirect(url_for('resPg', res_id=res_id))

    # Cannot find Restaurant
    return redirect(url_for('allResPg'))


# ========================
# Each Item (JSON)
@app.route(
    json_item_path.format(res_id='<int:res_id>', item_id='<int:item_id>'),
    methods=['GET'])
def itmJSON(res_id, item_id):
    '''Each Item in JSON format'''
    # Get restaurant
    res = db_session.query(Restaurant).filter_by(id=res_id).one()

    # Found Restaurant
    if res:

        # Get item
        item = db_session.query(MenuItem).filter_by(
                id=item_id,
                restaurant_id=res_id
            ).one()

        # Found Item
        if item:

            return jsonify(MenuItem=item.serialize)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>

# Assigning user from session
def createUser():
    '''Create new User'''
    newUser = User(
            name=session['username'],
            email=session['email'],
            picture=session['picture']
        )
    db_session.add(newUser)
    db_session.commit()

def getUser(user_id):
    '''Get User Information from User ID'''
    user = db_session.query(User).filter_by(id=user_id).one()
    return user

def getUserID():
    '''Get User ID number from ``session['email']``'''
    try:
        user = db_session.query(User).filter_by(email=session['email']).first()
        return user.id
    except:
        return None

# Start server when this file is run
if __name__ == '__main__':
    app.secret_key = 'very_secure_password'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
