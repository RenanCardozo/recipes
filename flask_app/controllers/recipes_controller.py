from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe


# -------------------view for new recipe

@app.route('/recipes/new')
def create_view():
    if not "user_id" in session:
        return redirect('/')

    return render_template('new_recipe.html')


# -------------- action route to create the recipe
@app.route('/recipes/create', methods=['post'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    dict = {
        **request.form,
        'user_id': session['user_id']
    }

    Recipe.save(dict)
    return redirect('/dashboard')


# -------------------- route to view edit
@app.route('/recipes/edit/<int:id>')
def edit_view(id):
    if not "user_id" in session:
        return redirect('/')

    recipe = Recipe.get_one({'id': id})
    print(recipe)
    return render_template('/edit_view.html', recipe=recipe)

# ------------------- route to submit the edit


@app.route('/recipe/edit_recipe', methods=['post'])
def edit_submit():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/recipes/edit/{request.form['id']}")
    print(request.form)
    dict = {
        **request.form

    }
    Recipe.edit(dict)
    return redirect('/dashboard')

#-------------------- delete 
@app.route('/delete/recipe/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/')
    Recipe.delete({'id': id})
    return redirect('/dashboard')

#---------------------------- show recipie
@app.route('/recipe/<int:id>')
def show_recipe(id):
    if not 'user_id' in session:
        return redirect('/')
    data ={
        'id': id
    }
    
    recipe = Recipe.get_one(data)
    return render_template("recipe_view.html", recipe = recipe)