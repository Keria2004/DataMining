import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

def load_and_process_data(file_path):
    df = pd.read_csv(file_path)

    # Tách nguyên liệu từ chuỗi 'a, b, c' thành list ['a', 'b', 'c']
    df['ingredients'] = df['ingredients'].apply(
        lambda x: [i.strip().lower() for i in str(x).split(',')] if pd.notna(x) else []
    )

    # Ghép lại thành chuỗi để sử dụng cho TF-IDF
    df['ingredients_str'] = df['ingredients'].apply(lambda lst: ' '.join(lst))

    return df

def apply_kmeans(df, n_clusters=5):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['ingredients_str'])

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(X)

    return df, vectorizer, X

def get_ingredients_list(df):
    ingredients_list = (
        df['ingredients']
        .explode()
        .dropna()
        .str.strip()
        .str.lower()
        .drop_duplicates()
        .tolist()
    )
    return ingredients_list

def suggest_by_similarity(df, vectorizer, X, input_ings, top_k=10):
    if not input_ings:
        return df.head(top_k)

    user_input_str = ' '.join(input_ings).lower()
    user_vec = vectorizer.transform([user_input_str])

    similarities = cosine_similarity(user_vec, X).flatten()
    df['similarity'] = similarities

    return df[df['similarity'] > 0].sort_values(by='similarity', ascending=False).head(top_k)


def recommend_from_favorites(favorite_recipes, all_recipes, n_clusters=5, n_recommend=10):
    documents = [r['ingredients'] if isinstance(r['ingredients'], str) else ' '.join(r['ingredients']) for r in all_recipes]
    
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(documents)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(X)
    labels = kmeans.labels_

    favorite_ids = set(r['id'] for r in favorite_recipes)

    # Xác định cluster trung tâm của món yêu thích (lấy cluster có nhiều món yêu thích nhất)
    favorite_indices = [i for i, r in enumerate(all_recipes) if r['id'] in favorite_ids]
    favorite_clusters = labels[favorite_indices]
    from collections import Counter
    most_common_cluster = Counter(favorite_clusters).most_common(1)[0][0]

    # Lọc món trong cluster đó nhưng chưa có trong yêu thích
    candidate_indices = [i for i, label in enumerate(labels) if label == most_common_cluster and all_recipes[i]['id'] not in favorite_ids]

    # Lấy tối đa n_recommend món gợi ý
    recommended = [all_recipes[i] for i in candidate_indices[:n_recommend]]

    return recommended
