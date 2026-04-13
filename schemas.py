from pydantic import BaseModel
from typing import Optional, List, Dict

class UserLogin(BaseModel):
    email: str
    password: str

class UserSignup(BaseModel):
    name: str
    email: str
    password: str

class SearchRequest(BaseModel):
    ingredients: List[str]
    preferences: Optional[dict] = {}
    offset: Optional[int] = 0

class RecommendRequest(BaseModel):
    user_id: Optional[str] = None
    mood: Optional[str] = None
    weather: Optional[str] = None
    offset: Optional[int] = 0

class ChatRequest(BaseModel):
    message: str
    context: Optional[List] = []

class SaveRecipeRequest(BaseModel):
    user_id: str
    recipe_id: str

class Ingredient(BaseModel):
    name: str
    qty: str

class Recipe(BaseModel):
    id: str
    name: str
    image: str
    cuisine: str
    mealType: str
    cookingTime: int
    difficulty: str
    servings: int
    mood: str
    utensils: List[str]
    special: str
    calories: int
    protein: int
    carbs: int
    fat: int
    ingredients: List[Ingredient]
    steps: List[str]


# ── Smart Recipe Filtering Engine Schemas ────────────────────────────────────

class SmartSearchRequest(BaseModel):
    """
    Request body for the smart-filtered recipe search endpoint.
    Requires at least 5 ingredient strings.
    """
    ingredients: List[str]
    diet: Optional[str] = None           # vegetarian | vegan | gluten_free | dairy_free
    cuisine: Optional[str] = None        # e.g. "Italian", "Indian"
    max_time: Optional[int] = None       # Maximum cooking time in minutes
    max_results: int = 10                # Max recipes to return (default 10)

    class Config:
        json_schema_extra = {
            "example": {
                "ingredients": ["tomato", "onion", "garlic", "chicken", "rice", "salt"],
                "diet": "vegetarian",
                "cuisine": "Italian",
                "max_time": 30,
                "max_results": 10,
            }
        }
