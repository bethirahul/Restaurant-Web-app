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
2. Setup Database:
    - Run [``database_setup.py``](/database_setup.py) using Python to setup Database
    - Run [``initiating_db_with_users.py``](/initiating_db_with_users.py) using Python to populate the database with values.
3. Run [``flask_app.py``](/flask_app.py) using Python, the app will be up and running on [localhost:8000](http://localhost:8000) address. Press **Ctrl**+**C** a few times to stop the server.
4. To be able to use Google and Facebook OAuth 2.0 Authentication, client id and client secret are needed from each of the providers. Populate these values inside:
    - Google - [``client_secret.json``](/client_secret.json)
    - Facebook - [``fb_client_secret.json``](/fb_client_secret.json)
5. There are two type of JSON endpoints for restaurants.
    - [``/restaurants/json``](http://localhost:8000/restaurants/json) - for all Restaurnts' Name, ID and creater ID
    - ``/restaurants/``_\<Restaurant ID>_``/json`` - for each Restaruant's Items

#### My LinkedIn profile

https://www.linkedin.com/in/rahulbethi