root_cnt = '''<!DOCTYPE html>
  <title>Message Board</title>
  <a href="{0}">Show Restaurants</a><br><br>
  <form method="POST">
    <textarea name="message"></textarea><br>
    <button type="submit">Post it!</button>
  </form>
  <pre>
{1}
  </pre>
</html>
'''

#========================
# Root - Home Page
rt_cnt = '''<!DOCTYPE html>
  <title>Restaurants - Home Page</title>
  <body>
    <h1>Restaurants Menu</h1>
    <a href="{all_res_path}">Show Restaurants</a>
  </body>
</html>
'''

#========================
# All Restaurants Page
all_res_cnt = '''<!DOCTYPE html>
  <title>Restaurants</title>
  <body>
    <h1>Restaurants:</h1><br>
    <a href="{add_res_path}">Add new Restaurant</a>
{all_res_cnt}
  </body>
</html>
'''
# each restaurant name with edit and delete
res_link_cnt = '''    <br><br>
    <a href="{res_path}">{res_name}</a><br>
    <a href="{edit_res_path}">Edit</a>
    <a href="{del_res_path}">Delete</a>
'''

#========================
# Each Restaurant Page
res_cnt = '''<!DOCTYPE html>
  <title>{res_name}</title>
  <body>
    <h3>{res_name}</h3>
    <a href="{all_res_path}">Go back</a><br>
    <br>
    <a href="{add_item_path}">Add Item</a><br>
    <br>
{res_items}
  </body>
</html>
'''
# each item in Restaurant page
res_item_cnt = '''    <p>
      {item_name}<br>
      {item_price}<br>
      {item_desc}
    </p>
    <a href="{edit_item_path}">Edit</a>
    <a href="{del_item_path}">Delete</a>
'''

#========================
# Add Restaurant Page
add_res_cnt = '''<!DOCTYPE html>
  <title>Add Restaurant</title>
  <body>
    <h3>Add a new Restaurant</h3>
    <a href="{all_res_path}">Go back</a><br>
    <br>
    <form method="POST">
      <input
        type="text"
        placeholder="Restaurant name"
        name="restaurant_name">
      <button type="submit">Add</button>
    </form>{error}
  </body>
</html>
'''
# field empty error
res_e_cnt = '''
    <p>Please fill in the restaurant name!</p>
'''

#========================
# Edit Restaurant Page
edit_res_cnt = '''<!DOCTYPE html>
  <title>Edit Restaurant</title>
  <body>
    <h4>Edit restaurant \'{res_name}\'</h4>
    <a href="{all_res_path}">Go back</a><br>
    <br>
    <form method="POST">
      <input
        type="text"
        placeholder="New restaurant name"
        name="restaurant_name">
      <button type="submit">Update</button>
    </form>{error}
  </body>
</html>
'''

#========================
# Delete Restaurant Page
del_res_cnt = '''<!DOCTYPE html>
  <title>Delete Restaurant</title>
  <body>
    <h4>Are you sure you want to delete restaurant \'{res_name}\'?</h4>
    <form method="POST">
      <input type="submit" value="Delete">
    </form><br>
    <a href="{all_res_path}">Go back</a>
  </body>
</html>
'''

#========================
# Add Item Page
add_item_cnt = '''<!DOCTYPE html>
  <title>Add Item</title>
  <body>
    <h3>Add a new Item in Restaurant \'{res_name}\'</h3>
    <a href="{res_path}">Go back</a><br>
    <br>
    <form method="POST">
      Name:
      <input
        type="text"
        placeholder="Item name"
        name="item_name"><br>
      <br>
      Price: $
      <input
        type="text"
        placeholder="Item price"
        name="item_price"><br>
      <br>
      Description:<br>
      <textarea
        placeholder="Item Description"
        name="message">
      </textarea><br>
      <br>
      <button type="submit">Add</button>
    </form>{error}
  </body>
</html>
'''
# field empty error
item_e_cnt = '''
    <p>Error: One of the fields is empty!</p>
'''

#========================
# Edit Item Page
edit_item_cnt = '''<!DOCTYPE html>
  <title>Edit Item</title>
  <body>
    <h3>Edit \'{item_name}\' in restaurant \'{res_name}\'</h3>
    <a href="{res_path}">Go back</a><br>
    <br>
    <h4>Present Name, Price and Description:</h4>
    <p>
      {item_name}<br>
      {item_price}<br>
      {item_desc}
    </p>
    <h4>Please update with new values below:</h4>
    <form method="POST">
      Name:
      <input
        type="text"
        placeholder="Item name"
        name="item_name"><br>
      <br>
      Price: $
      <input
        type="text"
        placeholder="Item price"
        name="item_price"><br>
      <br>
      Description:<br>
      <textarea
        placeholder="Item Description"
        name="message">
      </textarea><br>
      <br>
      <button type="submit">Update</button>
    </form>{error}
  </body>
</html>
'''

#========================
# Delete Restaurant Page
del_item_cnt = '''<!DOCTYPE html>
  <title>Delete Item</title>
  <body>
    <h4>Are you sure you want to delete item \'{item_name}\' from restaurant \'{res_name}\'?</h4>
    <form method="POST">
      <input type="submit" value="Delete">
    </form><br>
    <a href="{res_path}">Go back</a>
  </body>
</html>
'''