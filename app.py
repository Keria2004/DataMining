from flask import Flask, render_template, request
import pandas as pd
import ast

app = Flask(__name__)

# Load dataset
df = pd.read_csv('data/clean_dataset.csv')

# Convert ingredients column from string to list
df['ingredients'] = df['ingredients'].apply(ast.literal_eval)

# Extract all unique ingredients
ingredients_list = (
    df['ingredients']
    .explode()
    .dropna()
    .str.strip()
    .drop_duplicates()
    .tolist()
)

@app.route('/')
def index():
    return render_template("index.html", ingredients_list=ingredients_list, cuisines=[])


@app.route('/suggest', methods=['POST'])
def suggest():
    input_ingredients = request.form.get('ingredients', '').lower().split()
    input_ingredients = [i.strip() for i in input_ingredients if i.strip()]

    max_calories = request.form.get('calories')
    max_calories = int(max_calories) if max_calories else 9999

    def has_ingredient(row_ingredients):
        return any(ing.lower() in [i.lower() for i in row_ingredients] for ing in input_ingredients)

    filtered_df = df[
        df['ingredients'].apply(has_ingredient) & 
        (df['calories'] <= max_calories)
    ]

    cuisines = filtered_df[['name', 'cuisine', 'ingredients', 'calories', 'images']].to_dict(orient='records')

    return render_template('index.html', ingredients_list=ingredients_list, cuisines=cuisines)

if __name__ == '__main__':
    app.run(debug=True)
