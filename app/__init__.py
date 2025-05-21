from flask import Flask
from app.models import db  # ✅ Dùng lại instance từ models.py
from app.kmeans import load_and_process_data, apply_kmeans, get_ingredients_list
from app.main_routes import main_bp
from app.auth_routes import auth_bp
from app.favorite_routes import fav_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "super_secret_key"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # Load dữ liệu
    df = load_and_process_data("data/clean_dataset.csv")
    df.reset_index(drop=True, inplace=True)
    df['id'] = df.index
    df, vectorizer, X = apply_kmeans(df, n_clusters=5)
    ingredient_list = get_ingredients_list(df)

    # Gán vào app context
    app.df = df
    app.vectorizer = vectorizer
    app.X = X
    app.ingredient_list = ingredient_list

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(fav_bp)

    return app
