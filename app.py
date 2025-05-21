from flask import Flask, render_template, request
from kmeans import load_and_process_data, apply_kmeans, get_ingredients_list, suggest_by_similarity


app = Flask(__name__)

df = load_and_process_data("data/clean_dataset.csv")
df.reset_index(drop=True, inplace=True)  
df['id'] = df.index  
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

@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    # Lấy công thức từ df theo id
    recipe_row = df[df['id'] == recipe_id]
    if recipe_row.empty:
        return "Công thức không tồn tại", 404

    recipe = recipe_row.iloc[0].to_dict()

    # GỢI Ý THEO PHÂN CỤM (KMEANS)
    similar_recipes = df[
        (df['cluster'] == recipe['cluster']) & 
        (df['id'] != recipe_id)
    ].head(4).to_dict('records')

    # Chuẩn hóa lại nguyên liệu công thức để hiển thị
    ingredients_raw = recipe['ingredients']
    recipe_ingredients = (
        ingredients_raw if isinstance(ingredients_raw, list) 
        else [i.strip().lower() for i in ingredients_raw.split(',')]
    )
    recipe['ingredients'] = recipe_ingredients

    return render_template(
        "recipe.html",
        recipe=recipe,
        similar_recipes=similar_recipes
    )


if __name__ == "__main__":
    app.run(debug=True)
