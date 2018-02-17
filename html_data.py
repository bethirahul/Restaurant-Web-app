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

res_cnt = '''<!DOCTYPE html>
  <title>Restaurants</title>
  <body>
    <h1>Restaurants:</h1><br>
    <a href="{0}">Add new Restaurant</a><br><br>
    {1}
  </body>
</html>
'''

btn_cnt = '''    <p>
      {}
    </p>
    <a href="#">Edit</a>
    <a href="#">Delete</a>
    <br><br>
'''

add_res_cnt = '''<!DOCTYPE html>
  <title>Add Restaurant</title>
  <body>
    <h3>Add a new Restaurant</h3><br>
    <form method="POST">
      <input
        type="text"
        placeholder="Add restaurant name here"
        name="restaurant_name">
      <button type="submit">Add</button>
    </form>{0}<br>
    <a href="{1}">Go back</a>
  </body>
</html>
'''

add_res_e_cnt = '''
    <p>Please fill in the restaurant name!</p>
'''
