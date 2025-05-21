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
