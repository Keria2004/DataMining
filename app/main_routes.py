from flask import Blueprint, render_template, request, current_app
from app.kmeans import suggest_by_similarity
from flask import Blueprint, render_template, request, current_app, session, redirect, flash

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():

    if "username" not in session:
        flash("Bạn cần đăng nhập để sử dụng tính năng này.")
        return redirect("/login")

    df = current_app.df
    vectorizer = current_app.vectorizer
    X = current_app.X
    ingredient_list = current_app.ingredient_list

    user_input = ""
    recipes = []
    cuisine_filter = ""
    max_calories = ""

    if request.method == "POST":
        user_input = request.form.get("ingredients", "")
        cuisine_filter = request.form.get("cuisine", "").strip()
        max_calories = request.form.get("max_calories", "").strip()
        input_ings = [i.strip().lower() for i in user_input.split()]
        result_df = df.copy()

        if input_ings:
            result_df = suggest_by_similarity(result_df, vectorizer, X, input_ings)
        if cuisine_filter:
            result_df = result_df[result_df["cuisine"].str.lower() == cuisine_filter.lower()]
        if max_calories:
            try:
                max_val = float(max_calories)
                result_df = result_df[result_df["calories"].astype(float) <= max_val]
            except ValueError:
                pass

        recipes = result_df.to_dict("records")

    return render_template("index.html", ingredient_list=ingredient_list, ingredients=user_input, recipes=recipes)

@main_bp.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    df = current_app.df
    recipe_row = df[df['id'] == recipe_id]
    if recipe_row.empty:
        return "Công thức không tồn tại", 404

    recipe = recipe_row.iloc[0].to_dict()
    similar_recipes = df[(df['cluster'] == recipe['cluster']) & (df['id'] != recipe_id)].head(4).to_dict('records')

    ingredients_raw = recipe['ingredients']
    recipe_ingredients = ingredients_raw if isinstance(ingredients_raw, list) else [i.strip().lower() for i in ingredients_raw.split(',')]
    recipe['ingredients'] = recipe_ingredients

    return render_template("recipe.html", recipe=recipe, similar_recipes=similar_recipes)
