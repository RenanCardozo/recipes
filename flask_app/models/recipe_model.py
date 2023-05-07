from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model



class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.under30 = data['under30']
        self.description = data['description']
        self.instruction= data['instruction']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
        
        
        
    
    
    @classmethod
    def get_all(cls):
        query ='''
        SELECT * FROM recipes 
        JOIN users ON recipes.user_id = users.id;
        '''
        results = connectToMySQL(DATABASE).query_db(query)
        all_recipes = []
        if results:
            for row in results:
                this_recipe = cls(row)
                user_data = {
                    'id' : row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                    **row
                }
                this_user = user_model.User(user_data)
                this_recipe.planner = this_user
                all_recipes.append(this_recipe)
            return all_recipes
        
        return results
    
    @classmethod
    def edit(cls, data):
        query = '''
            UPDATE recipes SET name = %(name)s, under30 = %(under30)s, description = %(description)s , instruction = %(instruction)s ,date_made = %(date_made)s WHERE id = %(id)s;

        '''
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def save(cls, data):
        query = '''
            INSERT INTO recipes (name, under30, description, instruction, date_made, user_id) VALUES (%(name)s,%(under30)s,%(description)s,%(instruction)s,%(date_made)s,%(user_id)s)
        '''
        return connectToMySQL(DATABASE).query_db(query, data)
    
    
    @classmethod
    def get_one(cls, data):
        query= '''
            SELECT * FROM recipes  
            JOIN users ON recipes.user_id= users.id WHERE recipes.id = %(id)s;
        '''
        results = connectToMySQL(DATABASE).query_db(query, data)
        one_recipes =cls(results[0])
        for row in results:
            data ={
                **row,
                'id': row['users.id'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            users_recipe = user_model.User(data)
            one_recipes.poster = users_recipe
        return one_recipes
        
    @classmethod
    def delete(cls, data):
            query = "DELETE FROM recipes WHERE id = %(id)s;"
            return connectToMySQL(DATABASE).query_db(query, data)
        
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters","recipe")
        if len(recipe['instruction']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters","recipe")
        if len(recipe['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","recipe")
        if recipe['date_made'] == "":
            is_valid = False
            flash("Please enter a date","recipe")
        if not "under30" in recipe:
            is_valid = False
            flash("Please choose if under 30 minutes", 'recipe')
            
        return is_valid