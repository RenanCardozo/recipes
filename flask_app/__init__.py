from flask import Flask  # Import Flask to allow us to create our app
app = Flask(__name__)
DATABASE = "recipes_schema"
app.secret_key= "sdlkgj"