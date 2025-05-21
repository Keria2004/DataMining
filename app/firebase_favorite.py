from app.firebase_config import db

def get_favorites_by_user(username):
    favorites_ref = db.collection("favorites").where("username", "==", username)
    return [doc.to_dict() for doc in favorites_ref.stream()]

def toggle_favorite(username, recipe_id):
    fav_ref = db.collection("favorites").document(f"{username}_{recipe_id}")
    if fav_ref.get().exists:
        fav_ref.delete()
    else:
        fav_ref.set({
            "username": username,
            "recipe_id": recipe_id
        })
