from app import app, login
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Recipe
from app.classes.forms import RecipeForm
from flask_login import login_required
import datetime as dt
from bson.objectid import ObjectId

@app.route('/addingredient/,<recipeID>', methods=['GET','Post'])
def addingredient(recipeID):
    editRecipe = Recipe.objects.get(id=recipeID)
    form = IngredientForm()

    if form.validate_on_submit():
        editRecipe.ingredients.create(
            oid= ObjectId(),
            name= form.name.data,
            amount = form.amount.data,
            cost = form.cost.data
        )
        editRecipe.save()

        return redirect(url_for('recipe', recipeID = editRecipe.id))
        
    return render_template('editIngredient.html', form = form, editRecipe = editRecipe)


@app.route('/recipe/list')

@login_required

def recipeList():

    recipes = Recipe.objects()

    return render_template('recipes.html',recipes=recipes)

@app.route('/recipe/<recipeID>')

@login_required

def recipe(recipeID):

    thisRecipe = Recipe.objects.get(id=recipeID)

    return render_template('recipe.html',recipe=thisRecipe)

@app.route('/recipe/delete/<recipeID>')
# Only run this route if the user is logged in.
@login_required
def recipeDelete(recipeID):

    deleteRecipe = Recipe.objects.get(id=recipeID)

    if current_user == deleteRecipe.author:

        deleteRecipe.delete()

        flash('The Recipe was deleted.')
    else:

        flash("You can't delete a recipe you didn't create.")

    recipes = Recipe.objects()  

    return render_template('recipes.html',recipes=recipes)

@app.route('/recipe/new', methods=['GET', 'POST'])

@login_required

def recipeNew():

    form = RecipeForm()

     
    if form.validate_on_submit():

        newRecipe = Recipe(
            
            food_name = form.food_name.data,
            food_media = form.food_media.data,

            ingredient_name = form.ingredient_name.data,
            ingredient_amount = form.ingredient_amount.data,
            ingredient_cost = form.ingredient_cost.data,

            recipe_step = form.recipe_step.data,
            author = current_user.id,
            
            modifydate = dt.datetime.utcnow
        )

        newRecipe.save()

        return redirect(url_for('recipe',recipeID=newRecipe.id))

    
    return render_template('recipeform.html',form=form)


@app.route('/recipe/edit/<recipeID>', methods=['GET', 'POST'])
@login_required
def recipeEdit(recipeID):
    editRecipe = Recipe.objects.get(id=recipeID)
    
    
    if current_user != editRecipe.author:
        flash("You can't edit a recipe you don't own.")
        return redirect(url_for('recipe',recipeID=recipeID))
    
    form = RecipeForm()
    
    if form.validate_on_submit():
        
        editRecipe.update(
            food_name = form.food_name.data,
            ingredient_name = form.ingredient_name.data,
            ingredient_amount = form.ingredient_amount.data,
            ingredient_cost = form.ingredient_cost.data,
            recipe_step = form.recipe_step.data,
            author = current_user.id,
            modifydate = dt.datetime.utcnow
        )
        # This updates the profile image
        if form.food_media.data:
            if editRecipe.food_media:
                editRecipe.food_media.delete()
            editRecipe.food_media.put(form.food_media.data, content_type = 'image/jpeg')
            # This saves all the updates
            editRecipe.save()
        
        return redirect(url_for('recipe',recipeID=recipeID))

    

    form.food_name.data = editRecipe.food_name
    form.food_media.data = editRecipe.food_media

    form.ingredient_name.data = editRecipe.ingredient_name
    form.ingredient_amount.data = editRecipe.ingredient_amount
    form.ingredient_cost.data = editRecipe.ingredient_cost

    form.recipe_step.data = editRecipe.recipe_step
    

    return render_template('recipeform.html',form=form)