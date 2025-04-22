import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import ast

def load_and_process_data(file_path):
    # Load dataset
    df = pd.read_csv(file_path)

    # Chuyển cột 'ingredients' từ chuỗi sang danh sách
    df['ingredients'] = df['ingredients'].apply(ast.literal_eval)

    # Chuyển danh sách nguyên liệu thành chuỗi cho mỗi món ăn
    df['ingredients_str'] = df['ingredients'].apply(lambda x: ' '.join(x))

    return df

def apply_kmeans(df, n_clusters=5):
    # Sử dụng CountVectorizer để chuyển nguyên liệu thành ma trận đếm từ
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['ingredients_str'])

    # Áp dụng KMeans để phân nhóm món ăn
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(X)

    return df

def get_ingredients_list(df):
    # Tạo danh sách nguyên liệu duy nhất từ dataset
    ingredients_list = (
        df['ingredients']
        .explode()
        .dropna()
        .str.strip()
        .drop_duplicates()
        .tolist()
    )
    return ingredients_list
