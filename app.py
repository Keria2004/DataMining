from flask import Flask, render_template, request
import pandas as pd
from kmeans import load_and_process_data, apply_kmeans, get_ingredients_list, suggest_by_similarity

app = Flask(__name__)

# Tải dữ liệu & mô hình 1 lần khi khởi động
df = load_and_process_data("data/clean_dataset.csv")
df, vectorizer, X = apply_kmeans(df, n_clusters=5)
ingredient_list = get_ingredients_list(df)

@app.route("/", methods=["GET", "POST"])
def index():
    user_input = ""
    recipes = []

    if request.method == "POST":
        user_input = request.form.get("ingredients", "")
        input_ings = [i.strip().lower() for i in user_input.split()]
        recipes_df = suggest_by_similarity(df.copy(), vectorizer, X, input_ings)
        recipes = recipes_df.to_dict("records")

    return render_template(
        "index.html",
        ingredient_list=ingredient_list,
        ingredients=user_input,
        recipes=recipes
    )

if __name__ == "__main__":
    app.run(debug=True)
