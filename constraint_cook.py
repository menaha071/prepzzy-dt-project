"""
ConstraintCook AI — API Routes
Smart constraint-based recipe filtering using Spoonacular API as data source.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from ..services.constraint_engine import (
    constraint_search,
    filter_recipes_by_constraints,
    APPLIANCE_PROFILES,
    APPLIANCE_NAME_MAP,
    _get_safety_info,
    _normalize_text,
)

router = APIRouter(prefix="/api/constraint-cook", tags=["constraint-cook"])


# =========================================
# REQUEST MODELS
# =========================================

class ConstraintSearchRequest(BaseModel):
    """Request body for constraint-based recipe search."""
    ingredients: List[str]
    appliances: List[str]  # e.g., ["electric_kettle"], ["induction"], ["basic_setup"]
    maxTime: Optional[int] = None  # Max cooking time in minutes
    servings: Optional[int] = 1


class ConstraintFilterRequest(BaseModel):
    """Request body for filtering already-fetched recipes."""
    recipes: List[dict]
    appliances: List[str]
    maxTime: Optional[int] = None
    ingredients: Optional[List[str]] = []


# =========================================
# ENDPOINTS
# =========================================

@router.post("/search")
async def constraint_cook_search(data: ConstraintSearchRequest):
    """
    🎯 Main ConstraintCook AI endpoint.

    Flow:
    1. Fetches recipes from Spoonacular API based on ingredients
    2. Applies appliance-based filtering (keyword detection)
    3. Filters by simplicity and cooking time
    4. Ranks by ingredient match similarity
    5. Adds dynamic tags, power usage, and safety info
    6. Returns 3-5 best constraint-friendly recipes

    Returns closest matches if exact matches aren't found.
    """
    result = await constraint_search(
        ingredients=data.ingredients,
        appliances=data.appliances,
        max_time=data.maxTime,
        servings=data.servings or 1,
    )
    return result


@router.post("/filter")
async def constraint_cook_filter(data: ConstraintFilterRequest):
    """
    Filter an existing list of recipes through constraint logic.
    Useful for re-filtering without re-fetching from the API.
    """
    filtered = filter_recipes_by_constraints(
        recipes=data.recipes,
        appliances=data.appliances,
        max_time=data.maxTime,
        user_ingredients=data.ingredients,
    )
    return {
        "success": True,
        "recipes": filtered,
        "count": len(filtered),
        "inputCount": len(data.recipes),
        "filteredOut": len(data.recipes) - len(filtered),
    }


@router.get("/appliances")
async def get_appliances():
    """
    Get all supported appliance profiles with their constraints.
    Useful for building the frontend appliance selection UI.
    """
    profiles = []
    for key, profile in APPLIANCE_PROFILES.items():
        profiles.append({
            "id": key,
            "name": profile["display_name"],
            "powerLevel": profile["power_level"],
            "powerEmoji": profile["power_emoji"],
            "watts": profile["power_watts"],
            "safetyTips": profile["safety_tips"],
            "warnings": profile["warnings"],
        })
    return {"success": True, "appliances": profiles}


@router.get("/safety")
async def get_safety_tips(appliance: Optional[str] = None):
    """
    Get safety tips and warnings for specific appliances.
    Pass ?appliance=electric_kettle or ?appliance=induction.
    Without parameter, returns tips for all appliances.
    """
    if appliance:
        key = APPLIANCE_NAME_MAP.get(_normalize_text(appliance), appliance)
        keys = [key] if key in APPLIANCE_PROFILES else []
    else:
        keys = list(APPLIANCE_PROFILES.keys())

    if not keys:
        return {"success": False, "message": f"Unknown appliance: {appliance}"}

    safety = _get_safety_info(keys, "")
    return {
        "success": True,
        "appliance": appliance or "all",
        "safety": safety,
    }


@router.get("/power-guide")
async def get_power_guide():
    """
    Get power usage guide for all appliances.
    Helps students understand electricity consumption.
    """
    guide = []
    for key, profile in APPLIANCE_PROFILES.items():
        guide.append({
            "appliance": profile["display_name"],
            "powerLevel": profile["power_level"],
            "emoji": profile["power_emoji"],
            "watts": profile["power_watts"],
            "tip": _get_power_tip(profile["power_level"]),
        })
    return {"success": True, "guide": guide}


def _get_power_tip(level: str) -> str:
    """Get a power-saving tip based on power level."""
    tips = {
        "none": "Zero energy — perfect for late-night snacks without worrying about power!",
        "low": "Low energy draw — safe to use anytime, even during peak hours.",
        "medium": "Moderate energy — avoid using with other high-power appliances simultaneously.",
        "high": "High energy draw — use during off-peak hours. Don't combine with AC/heater.",
    }
    return tips.get(level, "Use responsibly.")
