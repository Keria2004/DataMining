from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from app.models import Favorite
from app import db
from preprocessing import find_recipe_by_id, recipes_data
from app.kmeans import recommend_from_favorites

fav_bp = Blueprint('favorite', __name__)

@fav_bp.route('/favorite/<int:recipe_id>', methods=['POST'])
@login_required
def toggle_favorite_route(recipe_id):
    user_id = current_user.id
    favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()

    if favorite:
        db.session.delete(favorite)
        action = "Xóa"
    else:
        new_fav = Favorite(user_id=user_id, recipe_id=recipe_id)
        db.session.add(new_fav)
        action = "Thêm"

    db.session.commit()
    print(f"{action} món yêu thích cho user {user_id}, recipe {recipe_id}")
    return '', 204

@fav_bp.route('/favorites')
@login_required
def show_favorites():
    user_id = current_user.id
    favorites = Favorite.query.filter_by(user_id=user_id).all()

    favorite_recipes = []
    for fav in favorites:
        recipe = find_recipe_by_id(fav.recipe_id)
        if recipe:
            favorite_recipes.append(recipe)

    recommendations = recommend_from_favorites(favorite_recipes, recipes_data)

    return render_template('favorites.html', favorites=favorite_recipes, recommendations=recommendations)
