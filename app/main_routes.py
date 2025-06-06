from flask import Blueprint, render_template, request, current_app, flash

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    df = current_app.df
    vectorizer = current_app.vectorizer
    X = current_app.X
    ingredient_list = current_app.ingredient_list

    user_input = ""
    recipes = []
    cuisine_filter = ""
    max_calories = ""

    if request.method == "POST":
        user_input = request.form.get("ingredients", "").strip()
        cuisine_filter = request.form.get("cuisine", "").strip()
        max_calories = request.form.get("max_calories", "").strip()
        input_ings = [i.lower() for i in user_input.split() if i.strip()]
        result_df = df.copy()

        if input_ings:
            from app.kmeans import suggest_by_similarity
            result_df = suggest_by_similarity(result_df, vectorizer, X, input_ings)

        if cuisine_filter:
            result_df = result_df[result_df["cuisine"].str.lower() == cuisine_filter.lower()]

        if max_calories:
            try:
                max_val = float(max_calories)
                result_df = result_df[result_df["calories"].astype(float) <= max_val]
            except ValueError:
                flash("Giá trị Calories không hợp lệ")

        recipes = result_df.to_dict("records")

    return render_template(
        "index.html",
        ingredient_list=ingredient_list,
        ingredients=user_input,
        recipes=recipes,
        cuisine=cuisine_filter,
        max_calories=max_calories,
    )

@main_bp.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    df = current_app.df
    recipe_row = df[df['id'] == recipe_id]

    if recipe_row.empty:
        return "Công thức không tồn tại", 404

    recipe = recipe_row.iloc[0].to_dict()

    # Lấy các món tương tự cùng cluster, loại trừ món đang xem, lấy 4 món
    similar_recipes = df[(df['cluster'] == recipe['cluster']) & (df['id'] != recipe_id)].head(4).to_dict('records')

    # Chuẩn hóa nguyên liệu thành list (nếu chưa phải list)
    ingredients_raw = recipe.get('ingredients', [])
    if isinstance(ingredients_raw, list):
        recipe_ingredients = ingredients_raw
    else:
        recipe_ingredients = [i.strip() for i in ingredients_raw.split(',') if i.strip()]
    recipe['ingredients'] = recipe_ingredients

    return render_template("recipe.html", recipe=recipe, similar_recipes=similar_recipes)
