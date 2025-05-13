import pandas as pd
import ast

# Đọc dữ liệu món ăn
df = pd.read_csv('data/clean_dataset.csv')

# Tiền xử lý cột 'ingredients'
transactions = []
for item in df['ingredients']:
    if pd.isna(item):
        continue
    try:
        ingredients = ast.literal_eval(item)
        ingredients = [ing.strip().lower() for ing in ingredients if ing.strip() != '']
        ingredients = list(set(ingredients))
        transactions.append(ingredients)
    except:
        continue

# One-hot encoding thủ công
all_ingredients = sorted({ingredient for transaction in transactions for ingredient in transaction})
import numpy as np
ingredients_onehot = pd.DataFrame(0, index=np.arange(len(transactions)), columns=all_ingredients)

for idx, ingredient_list in enumerate(transactions):
    ingredients_onehot.loc[idx, ingredient_list] = 1

# Lưu lại
ingredients_onehot.to_csv('data/ingredients_onehot.csv', index=False)

