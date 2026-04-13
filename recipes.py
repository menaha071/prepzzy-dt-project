from fastapi import APIRouter, HTTPException
from ..models.schemas import SearchRequest, RecommendRequest
from ..services.recipe_engine import search_recipes, get_recipe_by_id, get_recommendations
from ..services import spoonacular_service

router = APIRouter(prefix="/api", tags=["recipes"])


@router.post("/search-recipes")
async def search(data: SearchRequest):
    """
    Search recipes by ingredients.
    Tries Spoonacular API first for fresh, non-repeating results.
    Falls back to local recipe engine if API is unavailable.
    """
    # Try Spoonacular first
    if spoonacular_service.is_configured():
        results = await spoonacular_service.search_by_ingredients(
            ingredients=data.ingredients,
            preferences=data.preferences or {},
            offset=data.offset or 0,
        )
        if results:
            return {
                "success": True,
                "source": "spoonacular",
                "recipes": results,
                "count": len(results),
            }

    # Fallback to local engine
    results = search_recipes(data.ingredients, data.preferences or {})
    return {"success": True, "source": "local", "recipes": results, "count": len(results)}


@router.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: str):
    """
    Get full recipe details.
    Handles both Spoonacular IDs (sp-XXXXX) and local IDs.
    """
    # Check if it's a Spoonacular recipe ID
    if recipe_id.startswith("sp-"):
        sp_id = recipe_id.replace("sp-", "")
        try:
            sp_id_int = int(sp_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid Spoonacular recipe ID")

        if spoonacular_service.is_configured():
            recipe = await spoonacular_service.get_recipe_detail(sp_id_int)
            if recipe:
                return {"success": True, "source": "spoonacular", "recipe": recipe}

        raise HTTPException(status_code=404, detail="Recipe not found (API unavailable)")

    # Local recipe
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"success": True, "source": "local", "recipe": recipe}


@router.post("/recommend")
async def recommend(data: RecommendRequest):
    """
    Get personalized recipe recommendations.
    Tries Spoonacular for fresh, random results; falls back to local.
    """
    # Try Spoonacular first
    if spoonacular_service.is_configured():
        results = await spoonacular_service.get_recommendations(
            mood=data.mood,
            meal_type=None,  # Could be derived from weather
            number=8,
        )
        if results:
            return {"success": True, "source": "spoonacular", "recipes": results}

    # Fallback to local
    results = get_recommendations(data.mood, data.weather)
    return {"success": True, "source": "local", "recipes": results}


@router.get("/trending")
async def trending():
    """
    Get trending/random recipes for the dashboard.
    Uses Spoonacular's random endpoint for variety.
    """
    if spoonacular_service.is_configured():
        results = await spoonacular_service.get_random_recipes(number=8)
        if results:
            return {"success": True, "source": "spoonacular", "recipes": results}

    # Fallback to local
    results = get_recommendations()
    return {"success": True, "source": "local", "recipes": results}


@router.get("/status")
async def api_status():
    """Check if external APIs are configured."""
    key = spoonacular_service._get_api_key()
    return {
        "spoonacular_configured": spoonacular_service.is_configured(),
        "api_key_present": bool(key),
        "api_key_preview": key[:6] + "..." if key and len(key) > 6 else "(empty or placeholder)",
    }
