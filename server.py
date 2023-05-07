from flask_app.controllers import users_controller, recipes_controller
#each controller file must be imported into server for it to run 
from flask_app import app





if __name__ == '__main__':
    app.run(debug=True)