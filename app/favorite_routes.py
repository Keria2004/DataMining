from flask import Blueprint, session, redirect, flash, render_template
from functools import wraps
from app.firebase_favorite import toggle_favorite, get_favorites_by_user
from preprocessing import find_recipe_by_id , recipes_data
from app.kmeans import recommend_from_favorites

fav_bp = Blueprint("favorite", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("Bạn cần đăng nhập để tiếp tục.")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@fav_bp.route("/favorite/<int:recipe_id>", methods=["POST"])
@login_required
def toggle_favorite_route(recipe_id):
    username = session["username"]
    toggle_favorite(username, recipe_id)
    print(f"[DEBUG] Đã xử lý yêu thích cho {username} - Recipe {recipe_id}")
    return '', 204


@fav_bp.route("/favorites")
@login_required
def show_favorites():
    username = session["username"]
    favorites = get_favorites_by_user(username)
    favorite_recipes = [find_recipe_by_id(fav['recipe_id']) for fav in favorites if find_recipe_by_id(fav['recipe_id'])]

    # Gợi ý món mới dựa trên món yêu thích
    recommendations = recommend_from_favorites(favorite_recipes, recipes_data)

    return render_template("favorites.html", favorites=favorite_recipes, recommendations=recommendations)

