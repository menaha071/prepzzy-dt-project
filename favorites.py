from fastapi import APIRouter

_favorites = {}  # user_id -> list of recipe_ids

router = APIRouter(prefix="/api", tags=["favorites"])


@router.post("/save-recipe")
def save_recipe(data: dict):
    user_id = data.get("user_id", "anonymous")
    recipe_id = data.get("recipe_id")
    if user_id not in _favorites:
        _favorites[user_id] = []
    if recipe_id not in _favorites[user_id]:
        _favorites[user_id].append(recipe_id)
    return {"success": True, "favorites": _favorites[user_id]}


@router.get("/get-favorites/{user_id}")
def get_favorites(user_id: str):
    return {"success": True, "favorites": _favorites.get(user_id, [])}


@router.delete("/remove-favorite")
def remove_favorite(data: dict):
    user_id = data.get("user_id", "anonymous")
    recipe_id = data.get("recipe_id")
    if user_id in _favorites and recipe_id in _favorites[user_id]:
        _favorites[user_id].remove(recipe_id)
    return {"success": True}
