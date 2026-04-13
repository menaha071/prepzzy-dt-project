"""
Smart Recipe Filtering Service
Orchestrates the full pipeline: validate → normalize → fetch → match → filter →
deduplicate → rank → cache → return.
"""

import hashlib
import time
from typing import Any, Dict, List, Optional, Tuple

from ..utils.normalizer import normalize_list
from ..utils.matcher import calculate_match, MIN_MATCH_SCORE
from ..utils import deduplicator
from ..services import spoonacular_service

# ── In-memory TTL Cache ──────────────────────────────────────────────────────
_cache: Dict[str, Tuple[float, List[dict]]] = {}
CACHE_TTL = 300  # 5 minutes


def _cache_key(ingredients: List[str], filters: dict) -> str:
    """
    Build a deterministic cache key from sorted ingredients + filter params.
    Uses MD5 for compactness (not security-sensitive).
    """
    canonical = "|".join(sorted(ingredients)) + "||" + str(sorted(filters.items()))
    return hashlib.md5(canonical.encode()).hexdigest()


def _cache_get(key: str) -> Optional[List[dict]]:
    """Get from cache if not expired."""
    entry = _cache.get(key)
    if entry is None:
        return None
    timestamp, data = entry
    if time.time() - timestamp > CACHE_TTL:
        del _cache[key]
        return None
    return data


def _cache_set(key: str, data: List[dict]) -> None:
    """Store result in cache with current timestamp."""
    # Evict expired entries periodically (simple approach)
    now = time.time()
    expired_keys = [k for k, (ts, _) in _cache.items() if now - ts > CACHE_TTL]
    for k in expired_keys:
        del _cache[k]
    _cache[key] = (now, data)


def clear_cache() -> None:
    """Clear the entire result cache."""
    _cache.clear()


# ── Validation ───────────────────────────────────────────────────────────────

MIN_INGREDIENTS = 5


def validate_ingredients(ingredients: List[str]) -> Tuple[bool, str]:
    """
    Validate the ingredient list.
    Returns (is_valid, error_message).
    """
    if not ingredients:
        return False, "Ingredient list cannot be empty."

    # Filter out blank strings
    cleaned = [i.strip() for i in ingredients if i and i.strip()]

    if len(cleaned) < MIN_INGREDIENTS:
        return False, (
            f"At least {MIN_INGREDIENTS} ingredients are required. "
            f"You provided {len(cleaned)}."
        )

    return True, ""


# ── Dietary Filter ───────────────────────────────────────────────────────────

_DIET_FIELD_MAP = {
    "vegetarian": "vegetarian",
    "vegan": "vegan",
    "gluten_free": "glutenFree",
    "dairy_free": "dairyFree",
}


def _apply_dietary_filter(recipes: List[dict], diet: Optional[str]) -> List[dict]:
    """Filter recipes by dietary restriction flag."""
    if not diet:
        return recipes
    field = _DIET_FIELD_MAP.get(diet.lower().replace("-", "_").replace(" ", "_"))
    if not field:
        return recipes
    return [r for r in recipes if r.get(field, False)]


def _apply_cuisine_filter(recipes: List[dict], cuisine: Optional[str]) -> List[dict]:
    """Filter recipes by cuisine."""
    if not cuisine:
        return recipes
    target = cuisine.lower().strip()
    return [r for r in recipes if r.get("cuisine", "").lower() == target]


def _apply_time_filter(recipes: List[dict], max_time: Optional[int]) -> List[dict]:
    """Filter recipes by maximum cooking time (minutes)."""
    if not max_time or max_time <= 0:
        return recipes
    return [r for r in recipes if r.get("cookingTime", 999) <= max_time]


# ── Ranking ──────────────────────────────────────────────────────────────────

def _rank_recipes(recipes: List[dict]) -> List[dict]:
    """
    Sort recipes by:
      1. Highest match_score  (descending)
      2. Shorter cookingTime  (ascending)
      3. Fewer missing ingredients (ascending)
    """
    return sorted(
        recipes,
        key=lambda r: (
            -r.get("match_score", 0),
            r.get("cookingTime", 999),
            len(r.get("missing_ingredients", [])),
        ),
    )


# ── Smart Rejection ─────────────────────────────────────────────────────────

def _is_practical(recipe: dict, total_user: int) -> bool:
    """
    Reject recipes with too many missing ingredients.
    Rule: missing count must not exceed max(50% of user ingredients, 3).
    """
    missing_count = len(recipe.get("missing_ingredients", []))
    max_allowed = max(int(total_user * 0.5), 3)
    return missing_count <= max_allowed


# ── Main Pipeline ────────────────────────────────────────────────────────────

async def smart_search(
    ingredients: List[str],
    *,
    diet: Optional[str] = None,
    cuisine: Optional[str] = None,
    max_time: Optional[int] = None,
    max_results: int = 10,
) -> Dict[str, Any]:
    """
    Full smart-filtered recipe search pipeline.

    1. Validate input
    2. Normalize ingredients
    3. Check cache
    4. Fetch from Spoonacular API
    5. Match & score each recipe
    6. Filter by threshold (≥ 70%)
    7. Smart-reject impractical recipes
    8. Apply dietary / cuisine / time filters
    9. Deduplicate
    10. Rank
    11. Cache results
    12. Return

    Returns a dict with 'success', 'recipes', 'count', 'filters_applied', etc.
    """
    # 1. Validate
    is_valid, error_msg = validate_ingredients(ingredients)
    if not is_valid:
        return {
            "success": False,
            "error": error_msg,
            "recipes": [],
            "count": 0,
        }

    # 2. Normalize user ingredients
    normalized_user = normalize_list(ingredients)

    # Build filter dict for cache key
    filters = {}
    if diet:
        filters["diet"] = diet
    if cuisine:
        filters["cuisine"] = cuisine
    if max_time:
        filters["max_time"] = max_time

    # 3. Check cache
    c_key = _cache_key(normalized_user, filters)
    cached = _cache_get(c_key)
    if cached is not None:
        # Still apply max_results limit (user may request fewer)
        limited = cached[:max_results]
        return {
            "success": True,
            "source": "cache",
            "count": len(limited),
            "filters_applied": filters,
            "recipes": limited,
        }

    # 4. Fetch from Spoonacular
    preferences = {}
    if cuisine:
        preferences["cuisine"] = cuisine
    if max_time:
        preferences["cookingTime"] = str(max_time)

    raw_recipes = await spoonacular_service.search_by_ingredients(
        ingredients=ingredients,
        preferences=preferences,
        number=50,  # Fetch more to allow for filtering
    )

    if not raw_recipes:
        return {
            "success": True,
            "source": "spoonacular",
            "count": 0,
            "filters_applied": filters,
            "recipes": [],
            "message": "No recipes found from API. Try different ingredients.",
        }

    # 5 & 6. Match, score, and filter each recipe
    scored_recipes: List[dict] = []
    total_user = len(normalized_user)

    for recipe in raw_recipes:
        # Extract recipe ingredient names
        recipe_ing_names = [
            ing.get("name", "") for ing in recipe.get("ingredients", [])
        ]

        # Calculate match
        match_result = calculate_match(
            normalized_user, recipe_ing_names, pre_normalized=False
        )

        # Only include recipes meeting the threshold
        if not match_result.passes_threshold:
            continue

        # Annotate recipe with match data
        recipe["match_score"] = match_result.match_score
        recipe["matched_ingredients"] = match_result.matched_items
        recipe["missing_ingredients"] = match_result.missing_items
        recipe["extra_recipe_ingredients"] = match_result.extra_recipe_items
        recipe["matched_count"] = match_result.matched_count
        recipe["missing_count"] = len(match_result.missing_items)

        scored_recipes.append(recipe)

    # 7. Smart-reject impractical recipes
    scored_recipes = [r for r in scored_recipes if _is_practical(r, total_user)]

    # 8. Apply optional filters
    scored_recipes = _apply_dietary_filter(scored_recipes, diet)
    scored_recipes = _apply_cuisine_filter(scored_recipes, cuisine)
    scored_recipes = _apply_time_filter(scored_recipes, max_time)

    # 9. Deduplicate
    scored_recipes = deduplicator.deduplicate(scored_recipes)

    # 10. Rank
    scored_recipes = _rank_recipes(scored_recipes)

    # 11. Cache the full result set (before applying max_results)
    _cache_set(c_key, scored_recipes)

    # 12. Apply max_results and return
    limited = scored_recipes[:max_results]

    return {
        "success": True,
        "source": "spoonacular",
        "count": len(limited),
        "total_matched": len(scored_recipes),
        "filters_applied": filters,
        "recipes": limited,
    }
