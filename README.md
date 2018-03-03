# My Restaurant's Website (App)

This is a Restaurants Catalogue app, built by _**Rahul Bethi**_.

It is a **Web server** with a database to store and edit information about Restaurants and the food items sold in them.
It also has a user system with Google and Facebook **OAuth 2.0 authentication** to login and make modifications (**CRUD operations**) to _add_, _edit_ or _delete_ restaurants and their items.

It also has a JSON endpoint to provide restaurant details and item details

## Built using

- **Python 3.5.2** - **Flask** framework, **SQLAlchemy**, OAuth2, Jsonify
- Other tools used while building:
    - Vagrant - Ubuntu Linux - virtual machine
    - Postman
    - **HTML**, **CSS**
    - **Google**, **Facebook** OAuth 2.0 user login systems

## Instructions to run

1. Install **Python 3.5.2**, and then install:
    - ``flask``
    - ``sqlalchemy``
    - ``oauth2client``
    - ``httplib2``
2. Setup Database:
    - Run [``database_setup.py``](/database_setup.py) using Python to setup Database
    - Run [``initiating_db_with_users.py``](/initiating_db_with_users.py) using Python to populate the database with values.
3. Run [``flask_app.py``](/flask_app.py) using Python, the app will be up and running on [localhost:8000](http://localhost:8000) address. Press **Ctrl**+**C** a few times to stop the server.
4. To be able to use Google and Facebook OAuth 2.0 Authentication, App ID and Client Secret are needed from each of the providers. Populate these values inside:
    - Google - [``client_secret.json``](/client_secret.json)
    - Facebook - [``fb_client_secret.json``](/fb_client_secret.json)
5. There are two type of JSON endpoints for restaurants.
    - [``/restaurants/json``](http://localhost:8000/restaurants/json) - for all restaurnts' _name_, _ID_ and _creater ID_
    - ``/restaurants/``_\<``Restaurant ID``>_``/json`` - for each restaruant's items

## Design

1. [``database_setup.py``](/database_setup.py) uses SQLAlchemy library to setup database and tables inside it.
    - It has classes for tables and Columns in each table.
    - Serialize function in each class to return items in easily readable format - to convert to json.
    - Menu Item class also has time variable which stores the time when the item is created. This is used to sort the latest added items.

2. [``initiating_db_with_users.py``](/initiating_db_with_users.py) is used to populate the empty database which was created.

3. The server code [``flask_app.py``](/flask_app.py) is the main program.
    - It handles all the requests from the client, including Google and Facebook _OAuth 2.0_ Authentication.
        - Files [``client_secret.json``](/client_secret.json) for Google and [``initiating_db_with_users.py``](/initiating_db_with_users.py) for Facebook are used get the App ID and Client Secret for respective providers.
        - A Random string is generated and used to send and receive as state_token to avoid cross traffic session hijacking to add more security.
        - When a user log-in for the first time, A new entry is created in the database by getting the details of user's _name_, _profile picture_, _email_ and _ID_.
        - A returning user is identified using his _email_ address.

    - It also handles _CRUD operations_ (using SQLAlchemy) on the database which we created, based on the requests we get from client.
    - Two _Methods_ are supported, GET and POST as HTML5 only supports these two.
        - All links are accessed through GET method, only CRUD operations and login pages use POST method to submit the requests.

    - Flask framework is used to _handle requests_, send _**Flash messages**_ for errors, and render _**Dynamic HTML webpages**_.
    - _Please read through the code comments in [``flask_app.py``](/flask_app.py) for step by step explanation._

_Please read through the detailed code comments in [``flask_app.py``](/flask_app.py) to know how the app is built._

#### My LinkedIn profile

https://www.linkedin.com/in/rahulbethi