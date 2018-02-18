root_cnt = '''<!DOCTYPE html>
  <title>Message Board</title>
  <a href="{0}">Show Restaurants</a><br><br>
  <form method="POST">
    <textarea name="message"></textarea>
    <br>
    <button type="submit">Post it!</button>
  </form>
  <pre>
{1}
  </pre>
</html>
'''

rt_cnt = '''<!DOCTYPE html>
  <title>Restaurants - Home Page</title>
  <body>
    <h1>Restaurants Menu</h1>
    <a href="{all_res_path}">Show Restaurants</a>
  </body>
</html>
'''

all_res_cnt = '''<!DOCTYPE html>
  <title>Restaurants</title>
  <body>
    <h1>Restaurants:</h1>
    <br>
    <a href="{add_res_path}">Add new Restaurant</a>
    <br>
    <br>
    {all_res_cnt}
  </body>
</html>
'''

res_cnt = '''    <p>
      <a href="{res_path}">{res_name}</a>
    </p>
    <a href="{edit_res_path}">Edit</a>
    <a href="{del_res_path}">Delete</a>
    <br>
    <br>
'''

add_res_cnt = '''<!DOCTYPE html>
  <title>Add Restaurant</title>
  <body>
    <h3>Add a new Restaurant</h3><br>
    <form method="POST">
      <input
        type="text"
        placeholder="Restaurant name"
        name="restaurant_name">
      <button type="submit">Add</button>
    </form>{0}<br>
    <a href="{1}">Go back</a>
  </body>
</html>
'''

res_e_cnt = '''
    <p>Please fill in the restaurant name!</p>
'''

edit_res_cnt = '''<!DOCTYPE html>
  <title>Edit Restaurant</title>
  <body>
    <h4>Edit restaurant \'{0}\'</h4>
    <form method="POST">
      <input
        type="text"
        placeholder="New restaurant name"
        name="restaurant_name">
      <button type="submit">Update</button>
    </form>{1}<br>
    <a href="{2}">Go back</a>
  </body>
</html>
'''

del_res_cnt = '''<!DOCTYPE html>
  <title>Edit Restaurant</title>
  <body>
    <h4>Are you sure you want to delete restaurant \'{0}\'?</h4>
    <form method="POST">
      <input type="submit" value="Delete">
    </form><br>
    <a href="{1}">Go back</a>
  </body>
</html>
'''