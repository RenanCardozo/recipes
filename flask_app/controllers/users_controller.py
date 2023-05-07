from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



#--------------view login and register
@app.route('/')
def  sign_in():
    if 'user_id'  in session:
        return redirect('/dashboard')
    return render_template('index.html')

#--------------------- view dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data= {
        'id': session['user_id']
    }
    users = User.get_by_id(data)
    recipes = Recipe.get_all()
    return render_template('results.html', users = users , recipes= recipes)

# actioonnnnnnnnn route to login
@app.route('/login', methods=['post'])
def login():
    users= User.get_by_email(request.form)
    if not users:
        flash("Invalid email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(users.password, request.form['password']):
        flash("invalid password", 'login')
        return redirect('/')    
    session['user_id'] = users.id
    return redirect('/')


# actionnnnnnn route to register
@app.route('/register', methods=['post'])
def register():

    if not User.is_valid(request.form):
        return redirect('/')
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    print(user_id)
    session['user_id']= user_id
    return redirect('/dashboard' )



#actionnnnnn route to clear session and log out
@app.route('/logout')
def logout():
    session.clear()
    
    return redirect('/')