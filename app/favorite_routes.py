from flask import Blueprint, render_template, session, redirect, request, flash
from functools import wraps
from app.models import db, Favorite

fav_bp = Blueprint('favorite', __name__)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            flash("Bạn cần đăng nhập.")
            return redirect("/login")
        return f(*args, **kwargs)
    return wrap

@fav_bp.route("/favorites")
@login_required
def favorites():
    user_id = session['user_id']
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return render_template("favorites.html", favorites=favorites)

@fav_bp.route("/favorite/<int:recipe_id>", methods=["POST"])
@login_required
def toggle_favorite(recipe_id):
    user_id = session['user_id']
    fav = Favorite.query.filter_by(recipe_id=recipe_id, user_id=user_id).first()

    if fav:
        db.session.delete(fav)
    else:
        db.session.add(Favorite(recipe_id=recipe_id, user_id=user_id))
    db.session.commit()

    return redirect(request.referrer or "/")
