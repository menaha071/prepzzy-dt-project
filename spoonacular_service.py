"""
Spoonacular API Service
Wraps the Spoonacular Food API with data transformation to Prepzy's schema.
Falls back gracefully when API key is missing or requests fail.
"""

import os
import re
import random
from typing import Optional, List, Set, Dict
import httpx

SPOONACULAR_BASE = "https://api.spoonacular.com"


def _get_api_key() -> str:
    """Lazily read the API key so dotenv has time to load it."""
    return os.getenv("SPOONACULAR_API_KEY", "")


# Track seen recipe IDs to avoid repetition within a server session
_seen_ids: Set[int] = set()


def is_configured() -> bool:
    """Check if a valid Spoonacular API key is configured."""
    key = _get_api_key()
    return bool(key and key != "your_api_key_here")


def _strip_html(text: str) -> str:
    """Remove HTML tags from a string."""
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", text)


def _derive_difficulty(ready_minutes: int, ingredient_count: int) -> str:
    """Derive a difficulty level from cooking time and complexity."""
    score = ready_minutes + ingredient_count * 3
    if score < 40:
        return "Beginner"
    elif score < 70:
        return "Intermediate"
    return "Advanced"


def _derive_mood(dish_types: List[str], ready_minutes: int) -> str:
    """Derive a mood category from dish metadata."""
    types_lower = [t.lower() for t in dish_types] if dish_types else []
    if ready_minutes <= 15:
        return "Quick Snack"
    if any(t in types_lower for t in ["salad", "beverage", "drink"]):
        return "Light & Healthy"
    if any(t in types_lower for t in ["fingerfood", "appetizer", "snack"]):
        return "Party"
    return "Comfort Food"


def _derive_meal_type(dish_types: List[str]) -> str:
    """Derive meal type from Spoonacular's dishTypes."""
    if not dish_types:
        return "Dinner"
    types_lower = [t.lower() for t in dish_types]
    if any(t in types_lower for t in ["breakfast", "morning meal"]):
        return "Breakfast"
    if "lunch" in types_lower:
        return "Lunch"
    if any(t in types_lower for t in ["dinner", "main course", "main dish"]):
        return "Dinner"
    if any(t in types_lower for t in ["snack", "fingerfood", "appetizer", "antipasti", "starter", "hors d'oeuvre"]):
        return "Snacks"
    if any(t in types_lower for t in ["dessert", "sweet"]):
        return "Dessert"
    return "Dinner"


def _extract_nutrition(nutrition_data: dict) -> dict:
    """Extract calories, protein, carbs, fat from Spoonacular nutrition data."""
    result = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
    if not nutrition_data:
        return result

    nutrients = nutrition_data.get("nutrients", [])
    for n in nutrients:
        name_lower = n.get("name", "").lower()
        amount = round(n.get("amount", 0))
        if name_lower == "calories":
            result["calories"] = amount
        elif name_lower == "protein":
            result["protein"] = amount
        elif name_lower == "carbohydrates":
            result["carbs"] = amount
        elif name_lower == "fat":
            result["fat"] = amount

    return result


def _transform_recipe(sp_recipe: dict) -> dict:
    """Transform a Spoonacular recipe object into Prepzy's schema."""
    sp_id = sp_recipe.get("id", 0)

    # Extract ingredients
    ingredients = []
    for ing in sp_recipe.get("extendedIngredients", []):
        name = ing.get("name", ing.get("originalName", "Unknown"))
        # Use US measures for qty
        measures = ing.get("measures", {}).get("us", {})
        amount = measures.get("amount", ing.get("amount", ""))
        unit = measures.get("unitShort", ing.get("unit", ""))
        if amount and unit:
            qty = f"{amount} {unit}".strip()
        elif amount:
            qty = str(amount)
        else:
            qty = ing.get("original", "as needed")
        ingredients.append({"name": name.title(), "qty": qty})

    # Extract steps from analyzedInstructions
    steps = []
    analyzed = sp_recipe.get("analyzedInstructions", [])
    if analyzed:
        for instruction_group in analyzed:
            for step in instruction_group.get("steps", []):
                step_text = step.get("step", "").strip()
                if step_text:
                    steps.append(step_text)

    # If no analyzed instructions, try the `instructions` field
    if not steps and sp_recipe.get("instructions"):
        raw = _strip_html(sp_recipe["instructions"])
        # Split on sentence boundaries or numbered steps
        sentences = re.split(r'(?<=[.!])\s+', raw)
        steps = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]

    if not steps:
        steps = ["Follow the recipe instructions from the original source."]

    # Derive metadata
    cuisines = sp_recipe.get("cuisines", [])
    dish_types = sp_recipe.get("dishTypes", [])
    ready_minutes = sp_recipe.get("readyInMinutes", 30)

    # Extract nutrition
    nutrition = _extract_nutrition(sp_recipe.get("nutrition", {}))

    # Build image URL - Spoonacular provides full URLs
    image = sp_recipe.get("image", "")
    if image and not image.startswith("http"):
        image = f"https://img.spoonacular.com/recipes/{sp_id}-556x370.jpg"

    return {
        "id": f"sp-{sp_id}",
        "spoonacular_id": sp_id,
        "name": sp_recipe.get("title", "Untitled Recipe"),
        "image": image,
        "cuisine": cuisines[0] if cuisines else "International",
        "mealType": _derive_meal_type(dish_types),
        "cookingTime": ready_minutes,
        "difficulty": _derive_difficulty(ready_minutes, len(ingredients)),
        "servings": sp_recipe.get("servings", 4),
        "mood": _derive_mood(dish_types, ready_minutes),
        "utensils": [],  # Spoonacular doesn't provide this directly
        "special": _strip_html(sp_recipe.get("summary", ""))[:200] + "..." if sp_recipe.get("summary") else "A delicious recipe to try!",
        "calories": nutrition["calories"],
        "protein": nutrition["protein"],
        "carbs": nutrition["carbs"],
        "fat": nutrition["fat"],
        "ingredients": ingredients,
        "steps": steps,
        "sourceUrl": sp_recipe.get("sourceUrl", ""),
        "healthScore": sp_recipe.get("healthScore", 0),
        "vegetarian": sp_recipe.get("vegetarian", False),
        "vegan": sp_recipe.get("vegan", False),
        "glutenFree": sp_recipe.get("glutenFree", False),
        "dairyFree": sp_recipe.get("dairyFree", False),
    }


def _map_cuisine_filter(cuisine: str) -> str:
    """Map Prepzy cuisine names to Spoonacular supported cuisines."""
    mapping = {
        "South Indian": "Indian",
        "North Indian": "Indian",
        "Chinese": "Chinese",
        "Italian": "Italian",
        "Mexican": "Mexican",
        "Japanese": "Japanese",
        "Thai": "Thai",
        "Korean": "Korean",
        "Mediterranean": "Mediterranean",
        "American": "American",
        "French": "French",
        "Greek": "Greek",
        "Spanish": "Spanish",
        "Middle Eastern": "Middle Eastern",
        "Vietnamese": "Vietnamese",
    }
    return mapping.get(cuisine, cuisine)


def _map_meal_type_filter(meal_type: str) -> str:
    """Map Prepzy meal type names to Spoonacular's type parameter."""
    mapping = {
        "Breakfast": "breakfast",
        "Lunch": "main course",
        "Dinner": "main course",
        "Snacks": "snack",
        "Dessert": "dessert",
    }
    return mapping.get(meal_type, "")


async def search_by_ingredients(
    ingredients: List[str],
    preferences: dict = {},
    offset: int = 0,
    number: int = 20,
) -> List[dict]:
    """
    Search recipes by ingredients using Spoonacular's complexSearch.
    Uses addRecipeInformation and addRecipeNutrition to get full data in one call.
    """
    if not is_configured():
        return []

    params = {
        "apiKey": _get_api_key(),
        "includeIngredients": ",".join(ingredients),
        "addRecipeInformation": "true",
        "addRecipeNutrition": "true",
        "instructionsRequired": "true",
        "fillIngredients": "true",
        "sort": "max-used-ingredients",
        "number": number,
        "offset": offset,
    }

    # Apply preference filters
    if preferences.get("cuisine"):
        params["cuisine"] = _map_cuisine_filter(preferences["cuisine"])
    if preferences.get("mealType"):
        meal_type = _map_meal_type_filter(preferences["mealType"])
        if meal_type:
            params["type"] = meal_type
    if preferences.get("cookingTime"):
        time_map = {"15": 15, "30": 30, "60": 60, "60+": 999}
        max_time = time_map.get(preferences["cookingTime"], 999)
        if max_time < 999:
            params["maxReadyTime"] = max_time

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(f"{SPOONACULAR_BASE}/recipes/complexSearch", params=params)
            resp.raise_for_status()
            data = resp.json()

        results = []
        for sp_recipe in data.get("results", []):
            sp_id = sp_recipe.get("id", 0)
            transformed = _transform_recipe(sp_recipe)

            # Add match info similar to local engine
            used = sp_recipe.get("usedIngredientCount", 0)
            missed = sp_recipe.get("missedIngredientCount", 0)
            total = used + missed
            transformed["matchedIngredients"] = used
            transformed["totalIngredients"] = total
            transformed["score"] = used * 10 + (total - missed) * 3 if total > 0 else 0

            _seen_ids.add(sp_id)
            results.append(transformed)

        return results

    except Exception as e:
        print(f"[Spoonacular] Search failed: {e}")
        return []


async def get_recipe_detail(recipe_id: int) -> Optional[dict]:
    """
    Get full recipe details by Spoonacular recipe ID.
    """
    if not is_configured():
        return None

    params = {
        "apiKey": _get_api_key(),
        "includeNutrition": "true",
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(f"{SPOONACULAR_BASE}/recipes/{recipe_id}/information", params=params)
            resp.raise_for_status()
            sp_recipe = resp.json()

        return _transform_recipe(sp_recipe)

    except Exception as e:
        print(f"[Spoonacular] Get recipe {recipe_id} failed: {e}")
        return None


async def get_random_recipes(
    number: int = 8,
    tags: Optional[List[str]] = None,
) -> List[dict]:
    """
    Get random recipes for trending / recommendations.
    Uses include-tags for filtering (e.g., 'vegetarian', 'dessert').
    """
    if not is_configured():
        return []

    params = {
        "apiKey": _get_api_key(),
        "number": number,
        "includeNutrition": "true",
    }

    if tags:
        params["include-tags"] = ",".join(tags)

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(f"{SPOONACULAR_BASE}/recipes/random", params=params)
            resp.raise_for_status()
            data = resp.json()

        results = []
        for sp_recipe in data.get("recipes", []):
            sp_id = sp_recipe.get("id", 0)
            # Skip recipes we've already seen this session
            if sp_id in _seen_ids:
                continue
            _seen_ids.add(sp_id)
            results.append(_transform_recipe(sp_recipe))

        return results

    except Exception as e:
        print(f"[Spoonacular] Random recipes failed: {e}")
        return []


def _mood_to_tags(mood: str) -> List[str]:
    """Convert Prepzy mood to Spoonacular tags."""
    mapping = {
        "Comfort Food": [],  # No direct tag, return general
        "Light & Healthy": ["vegetarian"],
        "Party": ["fingerfood"],
        "Quick Snack": ["snack"],
    }
    return mapping.get(mood, [])


async def get_recommendations(
    mood: str = None,
    meal_type: str = None,
    number: int = 8,
) -> List[dict]:
    """
    Get personalized recipe recommendations based on mood/meal type.
    Uses Spoonacular's complexSearch with sort=random for variety.
    """
    if not is_configured():
        return []

    params = {
        "apiKey": _get_api_key(),
        "number": number,
        "addRecipeInformation": "true",
        "addRecipeNutrition": "true",
        "instructionsRequired": "true",
        "sort": "random",
    }

    if meal_type:
        sp_type = _map_meal_type_filter(meal_type)
        if sp_type:
            params["type"] = sp_type

    if mood:
        tags = _mood_to_tags(mood)
        if tags:
            params["diet"] = ",".join(tags)

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(f"{SPOONACULAR_BASE}/recipes/complexSearch", params=params)
            resp.raise_for_status()
            data = resp.json()

        results = []
        for sp_recipe in data.get("results", []):
            sp_id = sp_recipe.get("id", 0)
            if sp_id in _seen_ids:
                continue
            _seen_ids.add(sp_id)
            results.append(_transform_recipe(sp_recipe))

        return results

    except Exception as e:
        print(f"[Spoonacular] Recommendations failed: {e}")
        return []
