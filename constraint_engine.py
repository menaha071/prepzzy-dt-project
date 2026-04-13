"""
ConstraintCook AI — Smart Constraint Engine
Takes raw Spoonacular API recipes and applies intelligent post-processing:
  - Appliance-based filtering (keyword detection in instructions)
  - Simplicity filtering (step count, complexity)
  - Time filtering (under 10 min, 10-20 min)
  - Ingredient similarity ranking
  - Dynamic tagging (Kettle Only, No Flame, One-Pot Meal)
  - Power usage estimation
  - Safety & warning system
"""

from typing import List, Dict, Optional
import re


# =========================================
# BLOCKED / ALLOWED KEYWORD SETS
# =========================================

# Keywords that indicate a recipe CANNOT be made with limited appliances
BLOCKED_KEYWORDS = {
    "bake", "baking", "baked",
    "grill", "grilling", "grilled",
    "roast", "roasting", "roasted",
    "deep fry", "deep-fry", "deep fried", "deep-fried",
    "broil", "broiling", "broiled",
    "barbecue", "bbq",
    "smoke", "smoked", "smoking",
    "sear",
    "air fry", "air fryer",
    "pressure cook",  # most hostels won't have one
}

# Additional blocks specific to kettle-only mode
KETTLE_BLOCKED_KEYWORDS = {
    "fry", "frying", "fried",
    "sauté", "saute", "sautéed", "sauteed",
    "stir-fry", "stir fry",
    "pan", "skillet", "wok",
    "simmer",  # can't simmer in a kettle
}

# Keywords that are SAFE for simple/constrained cooking
ALLOWED_KEYWORDS = {
    "boil", "boiling", "boiled",
    "heat water", "hot water",
    "mix", "mixing", "stir", "stirring",
    "pour", "soak", "soaking",
    "chop", "dice", "slice", "cut",
    "mash", "crush",
    "blend", "whisk",
    "spread", "layer",
    "microwave",  # common in hostels
}

# Oven-related keywords (always blocked for constraint cooking)
OVEN_KEYWORDS = {
    "oven", "preheat", "preheated",
    "baking sheet", "baking tray", "baking pan",
    "casserole dish", "ramekin",
    "350°", "375°", "400°", "425°", "450°",
    "180°c", "200°c", "220°c",
}


# =========================================
# APPLIANCE PROFILES
# =========================================

APPLIANCE_PROFILES = {
    "electric_kettle": {
        "display_name": "Electric Kettle",
        "power_level": "low",
        "power_emoji": "⚡",
        "power_watts": "1000-1500W",
        "allowed_methods": {"boil", "heat water", "pour", "soak", "mix", "stir"},
        "blocked_methods": BLOCKED_KEYWORDS | KETTLE_BLOCKED_KEYWORDS,
        "safety_tips": [
            "⚡ Always place kettle on a flat, dry surface",
            "🔌 Unplug immediately after use to save power",
            "💧 Never overfill — water expands when boiling",
            "⚠️ Don't boil anything other than water unless multi-purpose kettle",
            "❌ Never open the lid while water is actively boiling",
            "🧹 Descale monthly with vinegar + water solution",
        ],
        "warnings": [
            "⚠️ Do not overload power sockets — use one high-wattage appliance at a time",
            "🔥 Handle with care — boiling water causes severe burns",
        ],
    },
    "induction": {
        "display_name": "Induction Stove",
        "power_level": "medium",
        "power_emoji": "⚡⚡",
        "power_watts": "1200-2000W",
        "allowed_methods": {"boil", "fry", "sauté", "stir-fry", "simmer", "heat", "cook", "scramble", "toast"},
        "blocked_methods": BLOCKED_KEYWORDS,
        "safety_tips": [
            "⚡ Use only induction-compatible (magnetic bottom) cookware",
            "🔌 Don't overload sockets — induction draws significant power",
            "💧 Keep the surface dry — water + electricity = danger",
            "⚠️ Don't place metal utensils on the surface when it's on",
            "🧹 Clean after every use — spills can damage the glass plate",
            "❌ Don't use if the glass surface is cracked",
            "⏱️ Avoid running during peak power hours in hostels",
        ],
        "warnings": [
            "⚠️ Do not overload sockets — induction uses 1200-2000W",
            "🔥 Pan handles get very hot — always use a cloth/mitt",
            "💨 Oil can splatter at high heat — keep a lid nearby",
        ],
    },
    "mixer_grinder": {
        "display_name": "Mixer Grinder",
        "power_level": "low",
        "power_emoji": "⚡",
        "power_watts": "500-750W",
        "allowed_methods": {"blend", "mix", "grind", "puree", "smoothie", "milkshake", "chutney", "crush"},
        "blocked_methods": BLOCKED_KEYWORDS | KETTLE_BLOCKED_KEYWORDS | {"boil", "heat", "simmer"},
        "safety_tips": [
            "⚡ Always secure the lid before starting",
            "🔌 Don't run continuously for more than 30 seconds — let the motor cool",
            "💧 Don't overfill — leave 1/3 space for blending action",
            "⚠️ Never put your hand inside when it's plugged in",
            "🧹 Wash immediately after use — dried food is hard to clean",
        ],
        "warnings": [
            "⚠️ Make sure mixer lid is on tight before blending",
            "🔌 Don't run for extended periods — motor can overheat",
        ],
    },
    "basic_setup": {
        "display_name": "Basic Setup (No Appliance)",
        "power_level": "none",
        "power_emoji": "🔋",
        "power_watts": "0W",
        "allowed_methods": {"mix", "stir", "chop", "slice", "mash", "spread", "pour", "soak"},
        "blocked_methods": BLOCKED_KEYWORDS | KETTLE_BLOCKED_KEYWORDS | {"boil", "heat"},
        "safety_tips": [
            "🔪 Use a cutting board — never cut on the desk or bed",
            "🧼 Wash hands before handling food",
            "🗑️ Dispose of peels and waste properly",
        ],
        "warnings": [
            "⚠️ Keep sharp utensils stored safely",
        ],
    },
}

# Map user-facing names to profile keys
APPLIANCE_NAME_MAP = {
    "electric kettle": "electric_kettle",
    "kettle": "electric_kettle",
    "electric_kettle": "electric_kettle",
    "induction": "induction",
    "induction stove": "induction",
    "induction_stove": "induction",
    "mixer": "mixer_grinder",
    "mixer grinder": "mixer_grinder",
    "mixer_grinder": "mixer_grinder",
    "blender": "mixer_grinder",
    "basic": "basic_setup",
    "basic setup": "basic_setup",
    "basic_setup": "basic_setup",
    "none": "basic_setup",
}


# =========================================
# INSTRUCTION ANALYSIS
# =========================================

def _normalize_text(text: str) -> str:
    """Lowercase and normalize text for keyword matching."""
    return text.lower().strip()


def _extract_all_instructions(recipe: dict) -> str:
    """Extract all instruction text from a recipe into a single string."""
    parts = []

    # From steps array
    for step in recipe.get("steps", []):
        parts.append(step)

    # From analyzedInstructions (Spoonacular raw)
    for group in recipe.get("analyzedInstructions", []):
        for step in group.get("steps", []):
            parts.append(step.get("step", ""))

    # From instructions field
    if recipe.get("instructions"):
        parts.append(recipe["instructions"])

    return _normalize_text(" ".join(parts))


def _check_blocked_keywords(instructions: str, blocked: set) -> List[str]:
    """Check if instructions contain any blocked cooking methods. Returns list of found blocked terms."""
    found = []
    for keyword in blocked:
        # Use word boundary matching to avoid false positives
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, instructions, re.IGNORECASE):
            found.append(keyword)
    return found


def _check_oven_required(instructions: str) -> bool:
    """Check if recipe requires an oven."""
    for keyword in OVEN_KEYWORDS:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, instructions, re.IGNORECASE):
            return True
    return False


# =========================================
# SIMPLICITY SCORING
# =========================================

def _calculate_simplicity_score(recipe: dict) -> float:
    """
    Score recipe simplicity from 0-100.
    Higher = simpler / more beginner-friendly.
    """
    score = 100.0

    # Step count penalty
    steps = recipe.get("steps", [])
    step_count = len(steps)
    if step_count > 10:
        score -= 30
    elif step_count > 7:
        score -= 15
    elif step_count > 5:
        score -= 5

    # Ingredient count penalty
    ingredients = recipe.get("ingredients", [])
    ing_count = len(ingredients)
    if ing_count > 12:
        score -= 25
    elif ing_count > 8:
        score -= 10
    elif ing_count > 5:
        score -= 3

    # Cooking time penalty
    cook_time = recipe.get("cookingTime", 30)
    if cook_time > 45:
        score -= 20
    elif cook_time > 30:
        score -= 10

    # Difficulty bonus/penalty
    difficulty = recipe.get("difficulty", "").lower()
    if difficulty == "beginner":
        score += 10
    elif difficulty == "advanced":
        score -= 20
    elif difficulty == "intermediate":
        score -= 5

    # Instruction complexity (average words per step)
    if steps:
        avg_words = sum(len(s.split()) for s in steps) / len(steps)
        if avg_words > 25:
            score -= 15  # complex instructions
        elif avg_words > 15:
            score -= 5

    return max(0, min(100, score))


def _is_simple_enough(recipe: dict, threshold: float = 40.0) -> bool:
    """Check if a recipe is simple enough for students/beginners."""
    return _calculate_simplicity_score(recipe) >= threshold


# =========================================
# INGREDIENT MATCHING
# =========================================

def _calculate_ingredient_match(user_ingredients: List[str], recipe: dict) -> dict:
    """
    Calculate how well user's ingredients match the recipe.
    Returns match stats and score.
    """
    user_lower = [ing.lower().strip() for ing in user_ingredients]

    recipe_ingredients = []
    for ing in recipe.get("ingredients", []):
        name = ing.get("name", "") if isinstance(ing, dict) else str(ing)
        recipe_ingredients.append(name.lower().strip())

    if not recipe_ingredients:
        return {"matched": 0, "total": 0, "missing": [], "score": 0}

    matched = 0
    missing = []

    for r_ing in recipe_ingredients:
        # Fuzzy matching — check if any user ingredient is contained in recipe ingredient or vice versa
        found = False
        for u_ing in user_lower:
            if u_ing in r_ing or r_ing in u_ing:
                found = True
                break
            # Also check individual words
            u_words = set(u_ing.split())
            r_words = set(r_ing.split())
            if u_words & r_words:  # any common words
                found = True
                break
        if found:
            matched += 1
        else:
            missing.append(r_ing.title())

    total = len(recipe_ingredients)
    # Score: weighted — full matches score higher, partial gets some credit
    match_ratio = matched / total if total > 0 else 0
    score = round(match_ratio * 100, 1)

    return {
        "matched": matched,
        "total": total,
        "missing": missing,
        "score": score,
    }


# =========================================
# DYNAMIC TAGGING
# =========================================

def _generate_tags(recipe: dict, appliance_keys: List[str], instructions: str) -> List[str]:
    """Generate dynamic constraint-aware tags for a recipe."""
    tags = []

    # Appliance-based tags
    if len(appliance_keys) == 1:
        if "electric_kettle" in appliance_keys:
            tags.append("Kettle Only")
        elif "basic_setup" in appliance_keys:
            tags.append("No Cooking")

    # No-flame detection
    has_flame_words = any(
        w in instructions
        for w in ["gas", "flame", "fire", "stove top", "gas burner"]
    )
    if not has_flame_words:
        tags.append("No Flame")

    # One-pot detection
    one_pot_indicators = ["one pot", "one-pot", "single pan", "all in one"]
    if any(ind in instructions for ind in one_pot_indicators):
        tags.append("One-Pot Meal")

    # Step count based tags
    steps = recipe.get("steps", [])
    if len(steps) <= 4:
        tags.append("Super Easy")

    # Time-based tags
    cook_time = recipe.get("cookingTime", 30)
    if cook_time <= 10:
        tags.append("Under 10 Min")
    elif cook_time <= 15:
        tags.append("Quick Fix")

    # Budget tag — simple heuristic based on ingredient count
    if len(recipe.get("ingredients", [])) <= 5:
        tags.append("Budget Friendly")

    # Dietary tags from Spoonacular data
    if recipe.get("vegetarian"):
        tags.append("Vegetarian")
    if recipe.get("vegan"):
        tags.append("Vegan")
    if recipe.get("glutenFree"):
        tags.append("Gluten Free")

    return tags


# =========================================
# POWER USAGE ESTIMATION
# =========================================

def _estimate_power_usage(appliance_keys: List[str], cook_time: int) -> dict:
    """Estimate power usage based on appliances and cooking time."""
    if not appliance_keys or "basic_setup" in appliance_keys and len(appliance_keys) == 1:
        return {
            "level": "none",
            "emoji": "🔋",
            "label": "No Power Needed",
            "estimated_watts": "0W",
            "warning": None,
        }

    # Use the highest-power appliance
    levels = {"low": 1, "medium": 2, "high": 3, "none": 0}
    max_level = "low"
    max_watts = "0W"

    for key in appliance_keys:
        profile = APPLIANCE_PROFILES.get(key)
        if profile:
            pl = profile["power_level"]
            if levels.get(pl, 0) > levels.get(max_level, 0):
                max_level = pl
                max_watts = profile["power_watts"]

    emoji_map = {"none": "🔋", "low": "⚡", "medium": "⚡⚡", "high": "⚡⚡⚡"}
    label_map = {"none": "No Power", "low": "Low Power", "medium": "Medium Power", "high": "High Power"}

    warning = None
    if max_level == "high" or (max_level == "medium" and cook_time > 20):
        warning = "⚠️ High power usage — avoid running during peak hours. Don't use multiple appliances simultaneously."
    elif max_level == "medium" and cook_time > 15:
        warning = "💡 Moderate power usage — be mindful of shared hostel electricity."

    return {
        "level": max_level,
        "emoji": emoji_map.get(max_level, "⚡"),
        "label": label_map.get(max_level, "Unknown"),
        "estimated_watts": max_watts,
        "warning": warning,
    }


# =========================================
# SAFETY SYSTEM
# =========================================

def _get_safety_info(appliance_keys: List[str], instructions: str) -> dict:
    """Generate safety tips and warnings based on appliances and recipe instructions."""
    tips = []
    warnings = []

    for key in appliance_keys:
        profile = APPLIANCE_PROFILES.get(key)
        if profile:
            tips.extend(profile["safety_tips"])
            warnings.extend(profile["warnings"])

    # Contextual warnings based on instruction content
    if "hot water" in instructions or "boiling" in instructions:
        warnings.append("🔥 Be careful with boiling water — it causes severe burns")
    if "oil" in instructions and ("heat" in instructions or "fry" in instructions):
        warnings.append("💨 Hot oil can splatter — keep a lid or plate nearby")
    if "knife" in instructions or "chop" in instructions or "dice" in instructions:
        warnings.append("🔪 Use a proper cutting board and keep fingers away from the blade")
    if "steam" in instructions:
        warnings.append("♨️ Hot steam can burn — always open lids away from your face")

    # Deduplicate
    tips = list(dict.fromkeys(tips))
    warnings = list(dict.fromkeys(warnings))

    return {"tips": tips, "warnings": warnings}


# =========================================
# MAIN CONSTRAINT FILTER
# =========================================

def filter_recipes_by_constraints(
    recipes: List[dict],
    appliances: List[str],
    max_time: Optional[int] = None,
    user_ingredients: Optional[List[str]] = None,
    simplicity_threshold: float = 40.0,
    result_limit: int = 5,
) -> List[dict]:
    """
    Apply all constraint filters to a list of Spoonacular recipes.

    Steps:
    1. Resolve appliance profiles
    2. Filter by appliance compatibility (keyword detection in instructions)
    3. Filter by simplicity
    4. Filter by cooking time
    5. Score by ingredient match
    6. Add tags, power usage, safety info
    7. Sort and return top results

    Args:
        recipes: Raw recipes from Spoonacular API (already transformed)
        appliances: User-selected appliances (e.g., ["electric_kettle", "induction"])
        max_time: Maximum cooking time in minutes (None = no limit)
        user_ingredients: Ingredients the user has available
        simplicity_threshold: Minimum simplicity score (0-100)
        result_limit: Max recipes to return (3-5)

    Returns:
        List of constraint-filtered, scored, tagged recipes
    """
    # Resolve appliance keys
    appliance_keys = []
    for a in appliances:
        key = APPLIANCE_NAME_MAP.get(_normalize_text(a))
        if key:
            appliance_keys.append(key)
    if not appliance_keys:
        appliance_keys = ["basic_setup"]

    # Build combined blocked keywords from all selected appliances
    # Use the MOST restrictive set (intersection would be too strict, union is right)
    # Actually: use the blocked set of the MOST LIMITED appliance
    combined_blocked = set()
    for key in appliance_keys:
        profile = APPLIANCE_PROFILES.get(key)
        if profile:
            combined_blocked |= profile["blocked_methods"]

    # If user has induction, un-block frying/sautéing (kettle blocks were added)
    if "induction" in appliance_keys:
        induction_allowed = APPLIANCE_PROFILES["induction"]["allowed_methods"]
        combined_blocked -= induction_allowed

    filtered = []

    for recipe in recipes:
        instructions = _extract_all_instructions(recipe)

        # --- FILTER 1: Oven check (always blocked) ---
        if _check_oven_required(instructions):
            continue

        # --- FILTER 2: Appliance-based keyword filtering ---
        blocked_found = _check_blocked_keywords(instructions, combined_blocked)
        if blocked_found:
            continue

        # --- FILTER 3: Time filtering ---
        cook_time = recipe.get("cookingTime", 30)
        if max_time is not None and cook_time > max_time:
            continue

        # --- FILTER 4: Simplicity filtering ---
        simplicity = _calculate_simplicity_score(recipe)
        if simplicity < simplicity_threshold:
            continue

        # --- SCORING ---
        score = 0.0

        # Ingredient match score (0-100, weighted at 50%)
        if user_ingredients:
            match_info = _calculate_ingredient_match(user_ingredients, recipe)
            ingredient_score = match_info["score"]
            recipe["ingredientMatch"] = match_info
        else:
            ingredient_score = 50  # neutral if no ingredients provided
            recipe["ingredientMatch"] = {"matched": 0, "total": 0, "missing": [], "score": 50}

        score += ingredient_score * 0.50

        # Simplicity score (0-100, weighted at 25%)
        score += simplicity * 0.25

        # Time bonus (weighted at 15%)
        time_score = max(0, 100 - cook_time * 2)  # shorter = higher
        score += time_score * 0.15

        # Step count bonus (weighted at 10%)
        step_count = len(recipe.get("steps", []))
        step_score = max(0, 100 - step_count * 8)
        score += step_score * 0.10

        recipe["constraintScore"] = round(score, 1)
        recipe["simplicityScore"] = round(simplicity, 1)

        # --- DYNAMIC TAGS ---
        recipe["constraintTags"] = _generate_tags(recipe, appliance_keys, instructions)

        # --- POWER USAGE ---
        recipe["powerUsage"] = _estimate_power_usage(appliance_keys, cook_time)

        # --- SAFETY INFO ---
        recipe["safetyInfo"] = _get_safety_info(appliance_keys, instructions)

        filtered.append(recipe)

    # Sort by constraint score (highest first)
    filtered.sort(key=lambda r: r.get("constraintScore", 0), reverse=True)

    # Return 3-5 results (at least 3 if available)
    limit = max(3, min(result_limit, 5))

    # If we have fewer than 3 results, relax simplicity threshold and retry
    if len(filtered) < 3:
        # Second pass with relaxed threshold
        relaxed = []
        for recipe in recipes:
            # Skip already included
            if any(r.get("id") == recipe.get("id") for r in filtered):
                continue

            instructions = _extract_all_instructions(recipe)
            if _check_oven_required(instructions):
                continue

            blocked_found = _check_blocked_keywords(instructions, combined_blocked)
            if blocked_found:
                continue

            cook_time = recipe.get("cookingTime", 30)
            if max_time is not None and cook_time > max_time:
                continue

            # Relaxed simplicity (half the threshold)
            simplicity = _calculate_simplicity_score(recipe)
            if simplicity < simplicity_threshold * 0.5:
                continue

            # Score with lower weight
            if user_ingredients:
                match_info = _calculate_ingredient_match(user_ingredients, recipe)
                recipe["ingredientMatch"] = match_info
                ingredient_score = match_info["score"]
            else:
                ingredient_score = 50
                recipe["ingredientMatch"] = {"matched": 0, "total": 0, "missing": [], "score": 50}

            score = ingredient_score * 0.50 + simplicity * 0.25
            recipe["constraintScore"] = round(score, 1)
            recipe["simplicityScore"] = round(simplicity, 1)
            recipe["constraintTags"] = _generate_tags(recipe, appliance_keys, instructions)
            recipe["constraintTags"].append("Closest Match")
            recipe["powerUsage"] = _estimate_power_usage(appliance_keys, cook_time)
            recipe["safetyInfo"] = _get_safety_info(appliance_keys, instructions)

            relaxed.append(recipe)

        relaxed.sort(key=lambda r: r.get("constraintScore", 0), reverse=True)
        filtered.extend(relaxed[:limit - len(filtered)])

    return filtered[:limit]


# =========================================
# HIGH-LEVEL SEARCH FUNCTION
# =========================================

async def constraint_search(
    ingredients: List[str],
    appliances: List[str],
    max_time: Optional[int] = None,
    servings: int = 1,
) -> dict:
    """
    Full ConstraintCook AI pipeline:
    1. Fetch recipes from Spoonacular API by ingredients
    2. Apply constraint-based filtering
    3. Return enriched, filtered results with tags + safety

    Args:
        ingredients: User's available ingredients
        appliances: Selected appliances
        max_time: Max cooking time filter
        servings: Number of servings

    Returns:
        Dict with filtered recipes, metadata, and safety info
    """
    from ..services import spoonacular_service

    # Resolve appliance keys for metadata
    appliance_keys = []
    for a in appliances:
        key = APPLIANCE_NAME_MAP.get(_normalize_text(a))
        if key:
            appliance_keys.append(key)
    if not appliance_keys:
        appliance_keys = ["basic_setup"]

    # Step 1: Fetch from Spoonacular (request more than we need for filtering headroom)
    raw_recipes = []
    if spoonacular_service.is_configured():
        # Fetch 20 recipes to have enough after filtering
        params = {}
        if max_time:
            params["cookingTime"] = str(max_time)
        raw_recipes = await spoonacular_service.search_by_ingredients(
            ingredients=ingredients,
            preferences=params,
            number=20,
        )

    # Step 1b: Fallback to local hostel recipes if API returns nothing
    source = "api"
    if not raw_recipes:
        try:
            from ..services.hostel_engine import HOSTEL_RECIPES
            raw_recipes = list(HOSTEL_RECIPES)  # copy so we don't mutate originals
            source = "local"
            print("[ConstraintCook] Spoonacular unavailable — falling back to local recipes")
        except Exception:
            raw_recipes = []

    if not raw_recipes:
        return {
            "success": False,
            "message": "No recipes found. Check your API key or try different ingredients.",
            "recipes": [],
            "count": 0,
            "appliances": [APPLIANCE_PROFILES.get(k, {}).get("display_name", k) for k in appliance_keys],
            "safetyTips": _get_safety_info(appliance_keys, ""),
        }

    # Step 2: Apply constraint filters
    filtered = filter_recipes_by_constraints(
        recipes=raw_recipes,
        appliances=appliances,
        max_time=max_time,
        user_ingredients=ingredients,
        simplicity_threshold=40.0,
        result_limit=5,
    )

    # Step 3: Build response metadata
    appliance_display = []
    for key in appliance_keys:
        profile = APPLIANCE_PROFILES.get(key)
        if profile:
            appliance_display.append({
                "name": profile["display_name"],
                "powerLevel": profile["power_level"],
                "powerEmoji": profile["power_emoji"],
                "watts": profile["power_watts"],
            })

    source_label = "API" if source == "api" else "curated local database"
    return {
        "success": True,
        "message": f"Found {len(filtered)} constraint-friendly recipes from {len(raw_recipes)} {source_label} results",
        "recipes": filtered,
        "count": len(filtered),
        "totalFetched": len(raw_recipes),
        "totalFiltered": len(raw_recipes) - len(filtered),
        "source": source,
        "appliances": appliance_display,
        "safetyTips": _get_safety_info(appliance_keys, ""),
        "filters": {
            "maxTime": max_time,
            "ingredientCount": len(ingredients),
            "applianceMode": appliance_keys,
        },
    }
