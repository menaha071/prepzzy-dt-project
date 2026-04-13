"""
Cook Lite Hostel — API Routes
Hostel-friendly recipe search, suggestions, safety, and freshness endpoints.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from ..services.hostel_engine import (
    search_hostel_recipes, get_suggestions, get_safety_tips,
    get_freshness_guide, get_storage_tips,
)

router = APIRouter(prefix="/api/hostel", tags=["hostel"])


class HostelSearchRequest(BaseModel):
    ingredients: List[str]
    appliances: List[str]
    servings: Optional[int] = 1
    maxTime: Optional[int] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None


@router.post("/search")
async def hostel_search(data: HostelSearchRequest):
    """Search hostel-friendly recipes by ingredients + appliances + filters."""
    results = search_hostel_recipes(
        ingredients=data.ingredients,
        appliances=data.appliances,
        servings=data.servings or 1,
        max_time=data.maxTime,
        tags=data.tags,
        category=data.category,
    )
    return {"success": True, "recipes": results, "count": len(results)}


@router.get("/suggestions")
async def hostel_suggestions(category: Optional[str] = None, limit: int = 5):
    """Get lifestyle-based recipe suggestions (midnight-snack, lazy-cooking, etc.)."""
    results = get_suggestions(category=category, limit=limit)
    return {"success": True, "recipes": results, "count": len(results)}


@router.get("/safety-tips")
async def hostel_safety(appliance: Optional[str] = None):
    """Get safety tips for specific or all appliances."""
    tips = get_safety_tips(appliance=appliance)
    return {"success": True, "tips": tips}


@router.get("/freshness-guide")
async def hostel_freshness():
    """Get food freshness detection guide."""
    guide = get_freshness_guide()
    return {"success": True, "guide": guide}


@router.get("/storage-tips")
async def hostel_storage():
    """Get storage and space optimization tips."""
    tips = get_storage_tips()
    return {"success": True, "tips": tips}
