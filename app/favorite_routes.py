from flask import Blueprint, request, jsonify, render_template, current_app
from app.kmeans import recommend_from_favorites

fav_bp = Blueprint('favorite', __name__)
favorites = set()

@fav_bp.route('/favorite/<int:recipe_id>', methods=['POST'])
def toggle_favorite_route(recipe_id):
    if recipe_id in favorites:
        favorites.remove(recipe_id)
        action = "removed"
    else:
        favorites.add(recipe_id)
        action = "added"
    print(f"{action} recipe {recipe_id}")
    return '', 204

@fav_bp.route('/favorites')
def show_favorites():
    df = current_app.df
    favorite_recipes = df[df['id'].isin(favorites)].to_dict('records')

    if favorite_recipes:
        recommendations = recommend_from_favorites(favorite_recipes, df.to_dict('records'))
    else:
        recommendations = []

    return render_template('favorites.html', favorites=favorite_recipes, recommendations=recommendations)