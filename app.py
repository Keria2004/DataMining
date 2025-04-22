# app.py
from flask import Flask, render_template, request
import pandas as pd
from kmeans import load_and_process_data, apply_kmeans, get_ingredients_list

app = Flask(__name__)

# Đọc dữ liệu và áp dụng KMeans
df = load_and_process_data('data/clean_dataset.csv')  # Đổi thành đường dẫn file của bạn
df = apply_kmeans(df, n_clusters=5)

# Lấy danh sách nguyên liệu duy nhất để hiển thị trong form
ingredients_list = get_ingredients_list(df)

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

    filtered_df = df[df['ingredients'].apply(has_ingredient) & (df['calories'] <= max_calories)]

    # Lọc món ăn theo nhóm (cluster) nếu có yêu cầu
    selected_cluster = request.form.get('cluster')
    if selected_cluster:
        filtered_df = filtered_df[filtered_df['cluster'] == int(selected_cluster)]

    cuisines = filtered_df[['name', 'cuisine', 'ingredients', 'calories', 'images', 'cluster']].to_dict(orient='records')

    return render_template('index.html', ingredients_list=ingredients_list, cuisines=cuisines)

if __name__ == '__main__':
    app.run(debug=True)
