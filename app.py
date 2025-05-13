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

    # Lấy form dữ liệu
    cuisine_filter = ""
    max_calories = ""

    if request.method == "POST":
        user_input = request.form.get("ingredients", "")
        cuisine_filter = request.form.get("cuisine", "").strip()
        max_calories = request.form.get("max_calories", "").strip()

        input_ings = [i.strip().lower() for i in user_input.split()]

        # Bắt đầu từ df gốc
        result_df = df.copy()

        # Gợi ý theo ingredients trước (vì cần tính similarity với toàn bộ X)
        if input_ings:
            result_df = suggest_by_similarity(result_df, vectorizer, X, input_ings)

        # Sau đó lọc theo cuisine (ưu tiên hiển thị)
        if cuisine_filter:
            result_df = result_df[result_df["cuisine"].str.lower() == cuisine_filter.lower()]

        # Cuối cùng lọc theo calories
        if max_calories:
            try:
                max_val = float(max_calories)
                result_df = result_df[result_df["calories"].astype(float) <= max_val]
            except ValueError:
                pass

        recipes = result_df.to_dict("records")


    return render_template(
        "index.html",
        ingredient_list=ingredient_list,
        ingredients=user_input,
        recipes=recipes
    )

if __name__ == "__main__":
    app.run(debug=True)
