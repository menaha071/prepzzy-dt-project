"""
Recipe Matching Engine
Implements weighted scoring algorithm for ingredient-to-recipe matching.
Designed to handle 250k+ recipes efficiently.
"""

import json
import os
import random

# Load recipe data
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes.json')

_recipes_cache = None

def _load_recipes():
    global _recipes_cache
    if _recipes_cache is not None:
        return _recipes_cache
    try:
        with open(DATA_PATH, 'r') as f:
            _recipes_cache = json.load(f)
    except FileNotFoundError:
        _recipes_cache = _generate_sample_recipes()
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        with open(DATA_PATH, 'w') as f:
            json.dump(_recipes_cache, f)
    return _recipes_cache


def _generate_sample_recipes():
    """Generate a rich sample dataset of recipes."""
    recipes = []
    
    base_recipes = [
        {"id": "si-1", "name": "Masala Dosa", "image": "https://images.unsplash.com/photo-1630383249896-424e482df921?w=600", "cuisine": "South Indian", "mealType": "Breakfast", "cookingTime": 30, "difficulty": "Intermediate", "servings": 4, "mood": "Comfort Food", "utensils": ["Tawa", "Kadai"], "special": "A crispy golden crepe filled with spiced potato masala.", "calories": 250, "protein": 6, "carbs": 40, "fat": 8, "ingredients": [{"name": "Rice", "qty": "2 cups"}, {"name": "Urad Dal", "qty": "1 cup"}, {"name": "Potato", "qty": "3 medium"}, {"name": "Onion", "qty": "2 medium"}, {"name": "Mustard Seeds", "qty": "1 tsp"}, {"name": "Curry Leaves", "qty": "10 leaves"}, {"name": "Turmeric", "qty": "1/2 tsp"}, {"name": "Green Chili", "qty": "3"}, {"name": "Oil", "qty": "3 tbsp"}, {"name": "Salt", "qty": "to taste"}], "steps": ["Soak rice and urad dal separately for 6 hours.", "Grind into smooth batter and ferment overnight.", "Boil and mash potatoes, prepare filling with spices.", "Heat tawa, spread batter, cook until crispy.", "Add potato filling and fold. Serve with chutney."]},
        {"id": "ni-1", "name": "Butter Chicken", "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=600", "cuisine": "North Indian", "mealType": "Dinner", "cookingTime": 45, "difficulty": "Intermediate", "servings": 4, "mood": "Comfort Food", "utensils": ["Kadai", "Oven"], "special": "Rich, creamy tomato-based curry with tender chicken.", "calories": 490, "protein": 32, "carbs": 15, "fat": 35, "ingredients": [{"name": "Chicken", "qty": "500g"}, {"name": "Yogurt", "qty": "1 cup"}, {"name": "Tomato", "qty": "4 large"}, {"name": "Butter", "qty": "4 tbsp"}, {"name": "Cream", "qty": "1/2 cup"}, {"name": "Onion", "qty": "2 large"}, {"name": "Ginger", "qty": "2 inch"}, {"name": "Garlic", "qty": "6 cloves"}, {"name": "Garam Masala", "qty": "1 tsp"}, {"name": "Salt", "qty": "to taste"}], "steps": ["Marinate chicken in yogurt and spices.", "Grill chicken until charred.", "Make tomato gravy with butter and spices.", "Add chicken to gravy, simmer with cream.", "Serve with naan."]},
        {"id": "ch-1", "name": "Fried Rice", "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=600", "cuisine": "Chinese", "mealType": "Lunch", "cookingTime": 20, "difficulty": "Beginner", "servings": 4, "mood": "Quick Snack", "utensils": ["Kadai"], "special": "Wok-tossed rice with vegetables and soy sauce.", "calories": 350, "protein": 10, "carbs": 52, "fat": 12, "ingredients": [{"name": "Rice", "qty": "3 cups cooked"}, {"name": "Egg", "qty": "2"}, {"name": "Carrot", "qty": "1"}, {"name": "Bell Pepper", "qty": "1"}, {"name": "Spring Onion", "qty": "4"}, {"name": "Soy Sauce", "qty": "2 tbsp"}, {"name": "Garlic", "qty": "4 cloves"}, {"name": "Oil", "qty": "3 tbsp"}, {"name": "Salt", "qty": "to taste"}], "steps": ["Use day-old rice for best results.", "Scramble eggs, set aside.", "Stir fry vegetables on high heat.", "Add rice and soy sauce.", "Toss with eggs and serve hot."]},
        {"id": "it-1", "name": "Margherita Pizza", "image": "https://images.unsplash.com/photo-1604382355076-af4b0eb60143?w=600", "cuisine": "Italian", "mealType": "Dinner", "cookingTime": 45, "difficulty": "Intermediate", "servings": 4, "mood": "Party", "utensils": ["Oven"], "special": "Classic pizza with tomato, mozzarella, and basil.", "calories": 420, "protein": 18, "carbs": 48, "fat": 18, "ingredients": [{"name": "All-Purpose Flour", "qty": "2.5 cups"}, {"name": "Yeast", "qty": "1 tsp"}, {"name": "Tomato", "qty": "4 large"}, {"name": "Mozzarella Cheese", "qty": "200g"}, {"name": "Basil", "qty": "10 leaves"}, {"name": "Olive Oil", "qty": "3 tbsp"}, {"name": "Salt", "qty": "1 tsp"}, {"name": "Garlic", "qty": "3 cloves"}], "steps": ["Make dough with flour, yeast, and water.", "Let rise for 2 hours.", "Stretch dough, add sauce and cheese.", "Bake at 250°C for 12-15 minutes.", "Top with fresh basil and serve."]},
        {"id": "it-2", "name": "Pasta Aglio e Olio", "image": "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=600", "cuisine": "Italian", "mealType": "Dinner", "cookingTime": 15, "difficulty": "Beginner", "servings": 4, "mood": "Quick Snack", "utensils": ["Kadai"], "special": "Simple garlic and olive oil pasta.", "calories": 380, "protein": 10, "carbs": 52, "fat": 16, "ingredients": [{"name": "Spaghetti", "qty": "400g"}, {"name": "Garlic", "qty": "8 cloves"}, {"name": "Olive Oil", "qty": "1/3 cup"}, {"name": "Red Chili Flakes", "qty": "1 tsp"}, {"name": "Parsley", "qty": "1/4 cup"}, {"name": "Salt", "qty": "to taste"}], "steps": ["Boil pasta until al dente.", "Slice and golden garlic in olive oil.", "Add chili flakes and pasta water.", "Toss pasta in the sauce.", "Serve with parsley."]},
        {"id": "ni-2", "name": "Palak Paneer", "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600", "cuisine": "North Indian", "mealType": "Lunch", "cookingTime": 35, "difficulty": "Beginner", "servings": 4, "mood": "Light & Healthy", "utensils": ["Kadai", "Mixer Grinder"], "special": "Creamy spinach gravy with paneer cubes.", "calories": 320, "protein": 18, "carbs": 12, "fat": 22, "ingredients": [{"name": "Spinach", "qty": "500g"}, {"name": "Paneer", "qty": "250g"}, {"name": "Onion", "qty": "1 large"}, {"name": "Tomato", "qty": "2"}, {"name": "Garlic", "qty": "4 cloves"}, {"name": "Cream", "qty": "2 tbsp"}, {"name": "Cumin Seeds", "qty": "1 tsp"}, {"name": "Salt", "qty": "to taste"}], "steps": ["Blanch and puree spinach.", "Fry paneer cubes until golden.", "Sauté onion and tomatoes.", "Add spinach puree and paneer.", "Finish with cream and serve."]},
        {"id": "mx-1", "name": "Tacos", "image": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=600", "cuisine": "Mexican", "mealType": "Dinner", "cookingTime": 30, "difficulty": "Beginner", "servings": 4, "mood": "Party", "utensils": ["Tawa"], "special": "Crispy tortillas with spiced filling.", "calories": 380, "protein": 24, "carbs": 28, "fat": 18, "ingredients": [{"name": "Tortilla", "qty": "8"}, {"name": "Chicken", "qty": "400g"}, {"name": "Onion", "qty": "1"}, {"name": "Tomato", "qty": "2"}, {"name": "Lime", "qty": "2"}, {"name": "Coriander Leaves", "qty": "1/4 cup"}, {"name": "Cumin Seeds", "qty": "1 tsp"}, {"name": "Salt", "qty": "to taste"}], "steps": ["Season and cook chicken.", "Dice onion, tomato, cilantro for salsa.", "Warm tortillas.", "Fill with chicken and toppings.", "Squeeze lime and serve."]},
        {"id": "th-1", "name": "Pad Thai", "image": "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=600", "cuisine": "Thai", "mealType": "Dinner", "cookingTime": 30, "difficulty": "Intermediate", "servings": 4, "mood": "Party", "utensils": ["Kadai"], "special": "Stir-fried noodles with peanuts and lime.", "calories": 420, "protein": 16, "carbs": 52, "fat": 18, "ingredients": [{"name": "Rice Noodles", "qty": "250g"}, {"name": "Egg", "qty": "2"}, {"name": "Tofu", "qty": "200g"}, {"name": "Peanuts", "qty": "1/4 cup"}, {"name": "Soy Sauce", "qty": "2 tbsp"}, {"name": "Sugar", "qty": "2 tbsp"}, {"name": "Lime", "qty": "1"}, {"name": "Bean Sprouts", "qty": "1 cup"}], "steps": ["Soak rice noodles.", "Make pad thai sauce.", "Fry tofu and eggs.", "Toss noodles with sauce.", "Serve with peanuts and lime."]},
    ]
    
    recipes.extend(base_recipes)
    
    # Generate additional recipes
    cuisines = ["South Indian", "North Indian", "Chinese", "Italian", "Mexican", "Japanese", "Thai", "Korean", "Mediterranean", "American", "French", "Greek", "Spanish", "Middle Eastern", "Vietnamese"]
    meals = ["Breakfast", "Lunch", "Dinner", "Snacks", "Dessert"]
    moods = ["Comfort Food", "Light & Healthy", "Party", "Quick Snack"]
    diffs = ["Beginner", "Intermediate", "Advanced"]
    
    # 100 diverse ingredients to create millions of permutations
    all_ingredients = [
        "Rice", "Onion", "Garlic", "Tomato", "Potato", "Chicken", "Egg", "Flour", "Butter", "Milk", 
        "Cheese", "Oil", "Salt", "Pepper", "Sugar", "Ginger", "Carrot", "Bell Pepper", "Spinach", "Lemon", 
        "Yogurt", "Bread", "Pasta", "Mushroom", "Corn", "Coconut", "Cumin", "Soy Sauce", "Paneer", "Cream",
        "Beef", "Pork", "Tofu", "Shrimp", "Salmon", "Tuna", "Lentils", "Chickpeas", "Black Beans", "Quinoa",
        "Oats", "Honey", "Maple Syrup", "Vanilla", "Cinnamon", "Nutmeg", "Basil", "Oregano", "Coriander", "Mint",
        "Rosemary", "Thyme", "Parsley", "Chili Flakes", "Paprika", "Turmeric", "Curry Powder", "Mustard", "Vinegar",
        "Olive Oil", "Sesame Oil", "Peanut Butter", "Almonds", "Walnuts", "Cashews", "Peanuts", "Pecans", "Chia Seeds",
        "Broccoli", "Cauliflower", "Zucchini", "Cabbage", "Kale", "Sweet Potato", "Pumpkin", "Eggplant", "Avocado",
        "Apple", "Banana", "Orange", "Strawberry", "Blueberry", "Raspberry", "Mango", "Pineapple", "Peach", "Plum",
        "Grapes", "Watermelon", "Melon", "Pomegranate", "Lime", "Bacon", "Sausage", "Ham", "Turkey", "Lamb"
    ]
    
    names_prefix = ["Spiced", "Roasted", "Grilled", "Crispy", "Creamy", "Fresh", "Classic", "Zesty", "Savory", "Sweet", "Smoky", "Tangy", "Hearty", "Light", "Rich"]
    names_suffix = ["Stew", "Stir Fry", "Curry", "Wrap", "Soup", "Salad", "Bowl", "Bites", "Fritters", "Risotto", "Tacos", "Flatbread", "Burger", "Omelette", "Parfait", "Pasta", "Casserole", "Skillet", "Bake", "Tart"]
    
    images = [
        "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600",
        "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=600",
        "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=600",
        "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600",
        "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600",
        "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=600",
        "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600",
        "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=600",
        "https://images.unsplash.com/photo-1490818387583-1baba5e638af?w=600",
        "https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?w=600"
    ]
    
    # Generate 1000 recipes!
    for i in range(1000):
        cuisine = cuisines[i % len(cuisines)]
        pref = names_prefix[(i * 3) % len(names_prefix)]
        suff = names_suffix[(i * 7) % len(names_suffix)]
        name = f"{cuisine} {pref} {suff}"
        
        n_ing = random.randint(5, 12)
        shuffled = random.sample(all_ingredients, n_ing)
        ingredients = [{"name": ing, "qty": f"{random.randint(1,3)} {random.choice(['cups', 'tbsp', 'pieces', 'tsp', 'oz'])}"} for ing in shuffled]
        
        recipes.append({
            "id": f"gen-{i+1}",
            "name": name,
            "image": images[i % len(images)],
            "cuisine": cuisine,
            "mealType": meals[i % len(meals)],
            "cookingTime": random.choice([10, 15, 20, 25, 30, 40, 45, 60]),
            "difficulty": diffs[i % len(diffs)],
            "servings": random.randint(1, 8),
            "mood": moods[i % len(moods)],
            "utensils": [random.choice(["Kadai", "Oven", "Tawa", "Induction", "Air Fryer", "Blender", "Wok", "Slow Cooker"])],
            "special": f"A delightful {cuisine.lower()} {name.lower()} featuring vibrant notes of {shuffled[0].lower()} and {shuffled[1].lower()}.",
            "calories": random.randint(150, 850),
            "protein": random.randint(4, 50),
            "carbs": random.randint(10, 85),
            "fat": random.randint(2, 45),
            "ingredients": ingredients,
            "steps": [
                f"Gather your {shuffled[0].lower()} and other fresh ingredients.",
                "Prep by chopping vegetables and measuring spices.",
                f"Heat oil in your {random.choice(['pan', 'pot', 'skillet'])} over medium heat.",
                f"Sauté the base ingredients until fragrant.",
                "Incorporate the remaining items and bring to a simmer.",
                "Cook until perfectly tender and flavors meld.",
                "Garnish with fresh herbs and serve immediately."
            ]
        })
    
    return recipes


def search_recipes(ingredients: list[str], preferences: dict = {}) -> list[dict]:
    """Search recipes by ingredients with weighted scoring."""
    recipes = _load_recipes()
    ingredient_list = [i.lower().strip() for i in ingredients]
    
    scored = []
    for recipe in recipes:
        recipe_ings = [i["name"].lower() for i in recipe["ingredients"]]
        
        # Exact matches
        exact = [i for i in ingredient_list if any(i in ri or ri in i for ri in recipe_ings)]
        # Partial word matches
        partial = [i for i in ingredient_list if any(
            any(w in i or i in w for w in ri.split())
            for ri in recipe_ings
        )]
        
        score = len(exact) * 10 + (len(partial) - len(exact)) * 3
        coverage = len(exact) / max(len(recipe_ings), 1)
        score += coverage * 20
        
        # Preference bonuses
        if preferences.get("cookingTime"):
            ct = preferences["cookingTime"]
            bounds = {"15": (0, 15), "30": (15, 30), "60": (30, 60), "60+": (60, 999)}
            lo, hi = bounds.get(ct, (0, 999))
            if lo <= recipe["cookingTime"] <= hi:
                score += 5
        if preferences.get("difficulty") and recipe["difficulty"] == preferences["difficulty"]:
            score += 5
        if preferences.get("cuisine") and recipe["cuisine"] == preferences["cuisine"]:
            score += 8
        if preferences.get("mealType") and recipe["mealType"] == preferences["mealType"]:
            score += 5
        if preferences.get("mood") and recipe["mood"] == preferences["mood"]:
            score += 5
        
        if score > 0:
            scored.append({
                **recipe,
                "score": score,
                "matchedIngredients": len(exact),
                "totalIngredients": len(recipe_ings),
            })
    
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:20]


from typing import Optional

def get_recipe_by_id(recipe_id: str) -> Optional[dict]:
    """Get a single recipe by ID."""
    recipes = _load_recipes()
    for r in recipes:
        if r["id"] == recipe_id:
            return r
    return None


def get_recommendations(mood: str = None, meal_type: str = None) -> list[dict]:
    """Get recipe recommendations based on mood and meal type."""
    recipes = _load_recipes()
    filtered = [
        r for r in recipes
        if (not mood or r.get("mood") == mood)
        and (not meal_type or r.get("mealType") == meal_type)
    ]
    random.shuffle(filtered)
    return filtered[:8]
