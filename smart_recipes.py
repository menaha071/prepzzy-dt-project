"""
Smart Recipe Filtering Engine — API Routes
Exposes smart-filtered recipe search with match scoring,
deduplication, and dietary/cuisine/time filters.
"""

from fastapi import APIRouter, HTTPException
from ..models.schemas import SmartSearchRequest
from ..services.smart_filter_service import smart_search, clear_cache
from ..utils import deduplicator

router = APIRouter(prefix="/api/smart-recipes", tags=["smart-recipes"])


@router.post("/search")
async def smart_recipe_search(data: SmartSearchRequest):
    """
    Smart-filtered recipe search.

    Accepts a list of ≥ 5 ingredients and returns recipes that match
    at least 70% of them. Results are deduplicated, ranked by match
    score / cooking time / missing ingredients, and optionally filtered
    by diet, cuisine, or maximum cooking time.
    """
    result = await smart_search(
        ingredients=data.ingredients,
        diet=data.diet,
        cuisine=data.cuisine,
        max_time=data.max_time,
        max_results=data.max_results,
    )

    if not result.get("success"):
        raise HTTPException(status_code=422, detail=result.get("error", "Invalid input."))

    return result


@router.get("/cache/clear")
async def clear_result_cache():
    """
    Clear the smart-recipe result cache and deduplication history.
    Useful for debugging or admin operations.
    """
    clear_cache()
    deduplicator.clear()
    return {
        "success": True,
        "message": "Smart recipe cache and deduplication history cleared.",
    }


@router.get("/stats")
async def smart_recipe_stats():
    """
    Return cache and deduplication statistics.
    """
    from ..services.smart_filter_service import _cache, CACHE_TTL
    import time

    active_entries = sum(
        1 for ts, _ in _cache.values() if time.time() - ts <= CACHE_TTL
    )

    return {
        "cache_entries": len(_cache),
        "active_cache_entries": active_entries,
        "cache_ttl_seconds": CACHE_TTL,
        "seen_recipe_ids": deduplicator.get_seen_count(),
    }
