import os
from flask import Flask
from app.kmeans import load_and_process_data, apply_kmeans, get_ingredients_list

global_df_container = {}

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super_secret_key'

    base_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    df = load_and_process_data("dataset/clean_dataset.csv")
    df.reset_index(drop=True, inplace=True)
    df['id'] = df.index
    df, vectorizer, X = apply_kmeans(df, n_clusters=5)
    ingredient_list = get_ingredients_list(df)

    # Gán thuộc tính dùng chung
    app.df = df
    app.vectorizer = vectorizer
    app.X = X
    app.ingredient_list = ingredient_list

    # Đăng ký blueprint
    from app.main_routes import main_bp
    from app.favorite_routes import fav_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(fav_bp)

    # Gán biến toàn cục để import từ app
    global_df_container['df'] = df

    return app

# Được dùng để import từ app import df
df = global_df_container.get('df')