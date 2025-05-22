import pandas as pd

# Load dữ liệu CSV 1 lần khi module được import
df_recipes = pd.read_csv("data/clean_dataset.csv")

# Tạo cột id dựa trên index
df_recipes['id'] = df_recipes.index.astype(str)

# Chuyển sang list dict dễ xử lý
recipes_data = df_recipes.to_dict(orient='records')


def find_recipe_by_id(recipe_id):
    for recipe in recipes_data:
        if str(recipe['id']) == str(recipe_id):
            return recipe
    return None

