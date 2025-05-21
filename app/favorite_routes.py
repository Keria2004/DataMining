from flask import Blueprint, render_template, session, redirect, request, flash, current_app
from functools import wraps
from app.firebase_favorite import get_favorites_by_user, toggle_favorite

fav_bp = Blueprint('favorite', __name__)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash("Bạn cần đăng nhập.")
            return redirect("/login")
        return f(*args, **kwargs)
    return wrap

@fav_bp.route("/favorites")
@login_required
def favorites():
    username = session["username"]
    favorites = get_favorites_by_user(username)

    # ✅ Lấy df từ current_app
    df = current_app.df
    recipe_list = []
    for fav in favorites:
        recipe_row = df[df["id"] == fav["recipe_id"]]
        if not recipe_row.empty:
            recipe_list.append(recipe_row.iloc[0].to_dict())

    return render_template("favorites.html", favorites=recipe_list)

@fav_bp.route("/favorite/<int:recipe_id>", methods=["POST"])
@login_required
def toggle_favorite_route(recipe_id):
    username = session["username"]
    toggle_favorite(username, recipe_id)
    return redirect(request.referrer or "/")
