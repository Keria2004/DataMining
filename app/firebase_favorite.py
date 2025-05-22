from app.firebase_config import db

def get_favorites_by_user(username):
    favorites_ref = db.collection("favorites").where("username", "==", username)
    docs = favorites_ref.stream()
    favorites = [doc.to_dict() for doc in docs]
    print(f"[DEBUG] Favorites of {username}: {favorites}")
    return favorites


def toggle_favorite(username, recipe_id):
    doc_id = f"{username}_{recipe_id}"
    ref = db.collection("favorites").document(doc_id)
    if ref.get().exists:
        ref.delete()
        print(f"Đã xóa favorite {doc_id}")
    else:
        ref.set({
            "username": username,
            "recipe_id": recipe_id
        })
        print(f"Đã thêm favorite {doc_id}")

