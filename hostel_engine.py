"""
Cook Lite Hostel — Recipe Engine
Curated hostel-friendly recipes with appliance-based filtering,
power usage tracking, safety tips, and beginner-focused cooking.
"""

from typing import List, Dict, Optional


# =========================================
# HOSTEL RECIPE DATABASE
# =========================================

HOSTEL_RECIPES = [
    # ---- KETTLE RECIPES ----
    {
        "id": "h-1", "name": "Kettle Maggi",
        "image": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=600",
        "appliances": ["kettle"], "cookingTime": 8, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "low", "tags": ["kettle-only", "no-flame", "midnight-snack", "budget", "one-pot"],
        "category": "quick-fix",
        "ingredients": [
            {"name": "Maggi Noodles", "qty": "1 pack"}, {"name": "Water", "qty": "1.5 cups"},
            {"name": "Maggi Masala", "qty": "1 sachet"}
        ],
        "steps": ["Boil water in the kettle.", "Put noodles and masala in a deep bowl.",
                  "Pour boiling water over noodles.", "Cover with a plate and wait 5 minutes.",
                  "Stir well and enjoy hot."],
        "tips": ["⚠️ Don't overfill the kettle — leave room for boiling.",
                 "💡 Break noodles into halves before adding for easier cooking.",
                 "🔥 Use a ceramic bowl, not plastic — hot water can warp plastic."],
        "safetyNotes": ["Keep kettle on a flat, dry surface.", "Unplug after use."],
        "calories": 350, "protein": 8, "carbs": 48, "fat": 14
    },
    {
        "id": "h-2", "name": "Boiled Eggs",
        "image": "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=600",
        "appliances": ["kettle"], "cookingTime": 12, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "low", "tags": ["kettle-only", "no-flame", "budget", "healthy-cheap"],
        "category": "healthy-cheap",
        "ingredients": [
            {"name": "Egg", "qty": "2-3"}, {"name": "Water", "qty": "enough to cover eggs"},
            {"name": "Salt", "qty": "a pinch"}
        ],
        "steps": ["Place eggs gently in the kettle.", "Fill with water to cover eggs.",
                  "Boil for 8-10 minutes for hard boiled.", "Carefully pour out hot water.",
                  "Run cold water over eggs, peel, and add salt."],
        "tips": ["⚠️ Don't boil more than 3 eggs at once in a kettle.",
                 "💡 Older eggs peel more easily than fresh ones.",
                 "🔥 Let eggs cool before peeling to avoid burns."],
        "safetyNotes": ["Be careful removing eggs — use a spoon.", "Don't let kettle boil dry."],
        "calories": 210, "protein": 18, "carbs": 1, "fat": 14
    },
    {
        "id": "h-3", "name": "Kettle Oats Porridge",
        "image": "https://images.unsplash.com/photo-1517673400267-0251440c45dc?w=600",
        "appliances": ["kettle"], "cookingTime": 7, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "low", "tags": ["kettle-only", "no-flame", "budget", "healthy-cheap"],
        "category": "healthy-cheap",
        "ingredients": [
            {"name": "Instant Oats", "qty": "1/2 cup"}, {"name": "Water or Milk", "qty": "1 cup"},
            {"name": "Honey", "qty": "1 tbsp"}, {"name": "Banana", "qty": "1 (optional)"}
        ],
        "steps": ["Boil water or milk in the kettle.", "Put oats in a bowl.",
                  "Pour hot liquid over oats, stir well.", "Cover for 3 minutes.",
                  "Add honey and sliced banana."],
        "tips": ["💡 Use instant oats, not steel-cut — they won't cook with just hot water.",
                 "⚠️ Stir immediately to prevent lumps.",
                 "🍯 Add honey after cooking, not during — keeps nutrients intact."],
        "safetyNotes": ["Careful pouring hot water — use a steady stream."],
        "calories": 220, "protein": 6, "carbs": 38, "fat": 5
    },
    {
        "id": "h-4", "name": "Cup Soup + Bread",
        "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=600",
        "appliances": ["kettle"], "cookingTime": 5, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "low", "tags": ["kettle-only", "no-flame", "midnight-snack", "budget"],
        "category": "lazy-cooking",
        "ingredients": [
            {"name": "Cup Soup Packet", "qty": "1"}, {"name": "Water", "qty": "200ml"},
            {"name": "Bread", "qty": "2 slices"}
        ],
        "steps": ["Boil water in the kettle.", "Empty soup packet into a mug.",
                  "Pour hot water and stir well for 30 seconds.", "Let it sit 1 minute.",
                  "Dip bread and enjoy."],
        "tips": ["💡 Stir vigorously to avoid lumps.", "⚠️ Don't add too much water — it'll be watery."],
        "safetyNotes": ["Use a ceramic mug — paper cups may leak with hot water."],
        "calories": 180, "protein": 4, "carbs": 28, "fat": 6
    },
    {
        "id": "h-5", "name": "Kettle Pasta",
        "image": "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=600",
        "appliances": ["kettle"], "cookingTime": 15, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "medium", "tags": ["kettle-only", "no-flame", "one-pot"],
        "category": "quick-fix",
        "ingredients": [
            {"name": "Penne/Fusilli Pasta", "qty": "1 cup"}, {"name": "Water", "qty": "2 cups"},
            {"name": "Salt", "qty": "1/2 tsp"}, {"name": "Tomato Ketchup", "qty": "2 tbsp"},
            {"name": "Chili Flakes", "qty": "1/2 tsp"}
        ],
        "steps": ["Boil water in kettle with salt.", "Add pasta to a deep bowl, pour boiling water.",
                  "Cover and wait 10 minutes, re-boil water and pour again if needed.",
                  "Drain water once pasta is soft.", "Mix in ketchup and chili flakes."],
        "tips": ["⚠️ Small pasta shapes cook faster — avoid spaghetti in a kettle.",
                 "💡 You may need to boil water twice for al dente pasta.",
                 "🔥 Drain carefully — use a plate to hold pasta while pouring water out."],
        "safetyNotes": ["Multiple boils will heat the kettle — let it rest between uses."],
        "calories": 320, "protein": 10, "carbs": 52, "fat": 6
    },
    {
        "id": "h-6", "name": "Hot Chocolate",
        "image": "https://images.unsplash.com/photo-1542990253-0d0f5be5f0ed?w=600",
        "appliances": ["kettle"], "cookingTime": 5, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "low", "tags": ["kettle-only", "no-flame", "midnight-snack"],
        "category": "lazy-cooking",
        "ingredients": [
            {"name": "Cocoa Powder / Hot Choco Mix", "qty": "2 tbsp"}, {"name": "Milk or Water", "qty": "1 cup"},
            {"name": "Sugar", "qty": "1-2 tsp"}
        ],
        "steps": ["Boil milk or water in the kettle.", "Add cocoa and sugar to a mug.",
                  "Pour hot liquid and stir vigorously.", "Enjoy warm."],
        "tips": ["💡 Mix cocoa with a little cold water first to prevent lumps.",
                 "⚠️ Don't boil milk directly in kettle if it has an auto-off sensor — it may trip."],
        "safetyNotes": ["Clean kettle after boiling milk to prevent residue buildup."],
        "calories": 150, "protein": 3, "carbs": 22, "fat": 6
    },

    # ---- INDUCTION RECIPES ----
    {
        "id": "h-7", "name": "Egg Bhurji (Scrambled Eggs)",
        "image": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=600",
        "appliances": ["induction"], "cookingTime": 10, "difficulty": "Beginner", "servings": 2,
        "powerUsage": "medium", "tags": ["no-flame", "budget", "quick-fix"],
        "category": "quick-fix",
        "ingredients": [
            {"name": "Egg", "qty": "3"}, {"name": "Onion", "qty": "1 small (chopped)"},
            {"name": "Tomato", "qty": "1 small (chopped)"}, {"name": "Green Chili", "qty": "1"},
            {"name": "Oil", "qty": "1 tbsp"}, {"name": "Salt", "qty": "to taste"},
            {"name": "Turmeric", "qty": "a pinch"}
        ],
        "steps": ["Heat oil on induction at medium.", "Add chopped onions, fry 2 min.",
                  "Add tomatoes and green chili, cook 2 min.", "Beat eggs with salt and turmeric.",
                  "Pour eggs in, scramble gently for 3-4 minutes.", "Serve with bread or roti."],
        "tips": ["⚠️ Keep heat on medium — high heat makes eggs rubbery.",
                 "💡 Don't stir too fast — let eggs set slightly before scrambling.",
                 "🧅 Add onions first, then tomatoes — onions need more time."],
        "safetyNotes": ["Use induction-compatible pan only.", "Keep water away from induction surface."],
        "calories": 280, "protein": 18, "carbs": 8, "fat": 20
    },
    {
        "id": "h-8", "name": "Poha (Flattened Rice)",
        "image": "https://images.unsplash.com/photo-1645177628172-a94c1f96e6db?w=600",
        "appliances": ["induction"], "cookingTime": 15, "difficulty": "Beginner", "servings": 2,
        "powerUsage": "medium", "tags": ["no-flame", "budget", "healthy-cheap"],
        "category": "healthy-cheap",
        "ingredients": [
            {"name": "Poha (Flattened Rice)", "qty": "1.5 cups"}, {"name": "Onion", "qty": "1 medium"},
            {"name": "Peanuts", "qty": "2 tbsp"}, {"name": "Mustard Seeds", "qty": "1/2 tsp"},
            {"name": "Curry Leaves", "qty": "5-6"}, {"name": "Turmeric", "qty": "1/4 tsp"},
            {"name": "Lemon", "qty": "1/2"}, {"name": "Oil", "qty": "2 tbsp"}, {"name": "Salt", "qty": "to taste"}
        ],
        "steps": ["Wash poha in water, drain, set aside for 5 min.", "Heat oil, add mustard seeds till they pop.",
                  "Add peanuts and curry leaves, fry 1 min.", "Add onions, cook till translucent.",
                  "Add turmeric and drained poha, mix gently.", "Cook on low for 3 min, squeeze lemon, serve."],
        "tips": ["⚠️ Don't soak poha too long — it'll turn mushy.",
                 "💡 Wash poha quickly under running water and drain immediately.",
                 "🍋 Add lemon juice at the end, not while cooking.",
                 "🥜 Fry peanuts till golden for best crunch."],
        "safetyNotes": ["Mustard seeds pop — keep a lid handy.", "Use medium heat to avoid burning."],
        "calories": 280, "protein": 8, "carbs": 42, "fat": 10
    },
    {
        "id": "h-9", "name": "Masala Omelette",
        "image": "https://images.unsplash.com/photo-1510693206972-df098062cb71?w=600",
        "appliances": ["induction"], "cookingTime": 8, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "low", "tags": ["no-flame", "budget", "quick-fix"],
        "category": "quick-fix",
        "ingredients": [
            {"name": "Egg", "qty": "2"}, {"name": "Onion", "qty": "1/4 (finely chopped)"},
            {"name": "Green Chili", "qty": "1 (chopped)"}, {"name": "Coriander Leaves", "qty": "1 tbsp"},
            {"name": "Salt", "qty": "to taste"}, {"name": "Oil/Butter", "qty": "1 tsp"}
        ],
        "steps": ["Beat eggs with onion, chili, coriander, and salt.", "Heat oil on induction at medium.",
                  "Pour egg mixture, spread evenly.", "Cook 2-3 min until bottom sets.",
                  "Flip carefully, cook 1 more minute.", "Fold and serve with bread."],
        "tips": ["⚠️ Don't flip too early — wait until edges are fully set.",
                 "💡 A non-stick pan makes flipping much easier.",
                 "🧈 Butter gives better flavor than oil for omelettes."],
        "safetyNotes": ["Handle hot pan carefully when flipping."],
        "calories": 220, "protein": 14, "carbs": 3, "fat": 16
    },
    {
        "id": "h-10", "name": "Induction Fried Rice",
        "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=600",
        "appliances": ["induction"], "cookingTime": 20, "difficulty": "Beginner", "servings": 2,
        "powerUsage": "medium", "tags": ["no-flame", "one-pot", "mess-alternative"],
        "category": "mess-alternative",
        "ingredients": [
            {"name": "Cooked Rice", "qty": "2 cups (leftover)"}, {"name": "Egg", "qty": "1"},
            {"name": "Onion", "qty": "1 small"}, {"name": "Carrot", "qty": "1/2 (diced)"},
            {"name": "Soy Sauce", "qty": "1.5 tbsp"}, {"name": "Oil", "qty": "2 tbsp"},
            {"name": "Salt", "qty": "to taste"}, {"name": "Pepper", "qty": "1/4 tsp"}
        ],
        "steps": ["Heat oil on high on induction.", "Scramble egg, push to side.",
                  "Add onion and carrot, stir-fry 3 min.", "Add cold rice, break lumps.",
                  "Add soy sauce and pepper, toss for 3-4 min.", "Serve hot."],
        "tips": ["💡 Use day-old cold rice — fresh rice gets sticky.",
                 "⚠️ Keep heat high for stir-frying — low heat makes it soggy.",
                 "🥕 Cut vegetables small so they cook quickly.",
                 "🧂 Go easy on soy sauce — it's very salty."],
        "safetyNotes": ["High heat cooking — keep face away from pan when stir-frying."],
        "calories": 380, "protein": 12, "carbs": 52, "fat": 14
    },
    {
        "id": "h-11", "name": "Dal Rice (Simple Lentil + Rice)",
        "image": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=600",
        "appliances": ["induction"], "cookingTime": 25, "difficulty": "Beginner", "servings": 2,
        "powerUsage": "high", "tags": ["no-flame", "budget", "one-pot", "healthy-cheap"],
        "category": "healthy-cheap",
        "ingredients": [
            {"name": "Toor Dal", "qty": "1/2 cup"}, {"name": "Rice", "qty": "1 cup"},
            {"name": "Water", "qty": "3 cups"}, {"name": "Turmeric", "qty": "1/4 tsp"},
            {"name": "Salt", "qty": "to taste"}, {"name": "Ghee", "qty": "1 tsp"}
        ],
        "steps": ["Wash dal and rice together.", "Add water, turmeric, and salt to pot.",
                  "Cook on induction at medium-high.", "Once boiling, reduce to low.",
                  "Cook 20 min till soft and mushy.", "Add ghee on top, mix and serve."],
        "tips": ["⚠️ Keep lid slightly open to prevent boiling over.",
                 "💡 Soak dal 15 min beforehand to cook faster.",
                 "🥄 Stir occasionally to prevent sticking at the bottom."],
        "safetyNotes": ["Hot steam when opening lid — open away from face.", "Monitor to prevent overflow."],
        "calories": 420, "protein": 16, "carbs": 68, "fat": 8
    },
    {
        "id": "h-12", "name": "Bread Toast + Butter",
        "image": "https://images.unsplash.com/photo-1509722747041-616f39b57569?w=600",
        "appliances": ["induction"], "cookingTime": 5, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "low", "tags": ["no-flame", "budget", "quick-fix"],
        "category": "lazy-cooking",
        "ingredients": [
            {"name": "Bread", "qty": "2 slices"}, {"name": "Butter", "qty": "1 tbsp"}
        ],
        "steps": ["Heat pan on induction at medium.", "Apply butter on one side of bread.",
                  "Place bread butter-side down on pan.", "Toast 1-2 min till golden.",
                  "Flip, toast other side, serve."],
        "tips": ["💡 Medium heat gives crispy toast — high heat burns it.",
                 "⚠️ Watch closely — toast goes from perfect to burnt in seconds."],
        "safetyNotes": ["Don't leave pan unattended on heat."],
        "calories": 200, "protein": 4, "carbs": 24, "fat": 10
    },
    {
        "id": "h-13", "name": "Upma",
        "image": "https://images.unsplash.com/photo-1630383249896-424e482df921?w=600",
        "appliances": ["induction"], "cookingTime": 18, "difficulty": "Beginner", "servings": 2,
        "powerUsage": "medium", "tags": ["no-flame", "budget", "healthy-cheap"],
        "category": "healthy-cheap",
        "ingredients": [
            {"name": "Semolina (Rava)", "qty": "1 cup"}, {"name": "Water", "qty": "2.5 cups"},
            {"name": "Onion", "qty": "1 small"}, {"name": "Mustard Seeds", "qty": "1/2 tsp"},
            {"name": "Green Chili", "qty": "1"}, {"name": "Oil", "qty": "2 tbsp"},
            {"name": "Salt", "qty": "to taste"}, {"name": "Lemon", "qty": "1/2"}
        ],
        "steps": ["Dry roast semolina on medium heat 3 min, set aside.", "Heat oil, add mustard seeds.",
                  "Add chopped onion and chili, fry 2 min.", "Add water and salt, bring to boil.",
                  "Slowly add roasted semolina while stirring continuously.",
                  "Cook on low 3-4 min, squeeze lemon, serve."],
        "tips": ["⚠️ Stir continuously while adding rava to prevent lumps — this is the most critical step!",
                 "💡 Dry roasting rava gives a nutty flavor and better texture.",
                 "🔥 Reduce heat before adding rava to boiling water.",
                 "🍋 Add lemon after switching off heat."],
        "safetyNotes": ["Hot water splatters when adding rava — stir from a distance."],
        "calories": 300, "protein": 8, "carbs": 44, "fat": 10
    },
    {
        "id": "h-14", "name": "Bread Pizza",
        "image": "https://images.unsplash.com/photo-1604382355076-af4b0eb60143?w=600",
        "appliances": ["induction"], "cookingTime": 10, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "low", "tags": ["no-flame", "midnight-snack", "quick-fix"],
        "category": "midnight-snack",
        "ingredients": [
            {"name": "Bread", "qty": "2 slices"}, {"name": "Tomato Ketchup", "qty": "2 tbsp"},
            {"name": "Onion", "qty": "1/4 (chopped)"}, {"name": "Capsicum", "qty": "1/4 (chopped)"},
            {"name": "Cheese", "qty": "2 slices or grated"}, {"name": "Oregano", "qty": "a pinch"},
            {"name": "Oil/Butter", "qty": "1 tsp"}
        ],
        "steps": ["Spread ketchup on bread slices.", "Add chopped onion, capsicum, and cheese.",
                  "Sprinkle oregano on top.", "Heat pan with butter on low-medium.",
                  "Place bread in pan, cover with lid for 3-4 min.", "Cheese melts, bottom crisps — serve hot."],
        "tips": ["⚠️ Keep heat LOW — otherwise bread burns before cheese melts.",
                 "💡 Cover with a lid so steam melts the cheese.",
                 "🧀 Grated cheese melts faster than sliced."],
        "safetyNotes": ["Use low flame. Keep lid on to trap heat evenly."],
        "calories": 280, "protein": 10, "carbs": 30, "fat": 14
    },
    {
        "id": "h-15", "name": "Vegetable Sandwich",
        "image": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=600",
        "appliances": ["induction"], "cookingTime": 8, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "low", "tags": ["no-flame", "budget", "quick-fix"],
        "category": "quick-fix",
        "ingredients": [
            {"name": "Bread", "qty": "4 slices"}, {"name": "Butter", "qty": "1 tbsp"},
            {"name": "Cucumber", "qty": "1/2 sliced"}, {"name": "Tomato", "qty": "1 sliced"},
            {"name": "Onion", "qty": "1/4 sliced"}, {"name": "Chaat Masala", "qty": "1/2 tsp"},
            {"name": "Salt", "qty": "to taste"}
        ],
        "steps": ["Apply butter on all bread slices.", "Layer cucumber, tomato, and onion.",
                  "Sprinkle chaat masala and salt.", "Place another bread slice on top.",
                  "Toast on pan or eat as-is."],
        "tips": ["💡 Pat dry cucumber slices to prevent soggy sandwich.",
                 "⚠️ Chaat masala makes a big difference — don't skip it!"],
        "safetyNotes": ["Standard cooking precautions."],
        "calories": 250, "protein": 6, "carbs": 32, "fat": 12
    },
    {
        "id": "h-16", "name": "Aloo Fry (Quick Potato Fry)",
        "image": "https://images.unsplash.com/photo-1600289031464-74d374b64991?w=600",
        "appliances": ["induction"], "cookingTime": 20, "difficulty": "Beginner", "servings": 2,
        "powerUsage": "medium", "tags": ["no-flame", "budget", "mess-alternative"],
        "category": "mess-alternative",
        "ingredients": [
            {"name": "Potato", "qty": "2 medium (diced)"}, {"name": "Onion", "qty": "1 small"},
            {"name": "Turmeric", "qty": "1/4 tsp"}, {"name": "Red Chili Powder", "qty": "1/2 tsp"},
            {"name": "Oil", "qty": "2 tbsp"}, {"name": "Salt", "qty": "to taste"}
        ],
        "steps": ["Dice potatoes small for fast cooking.", "Heat oil, add onions, fry 2 min.",
                  "Add potatoes, turmeric, chili, salt.", "Cover and cook on medium-low 12-15 min.",
                  "Stir every 3-4 min to prevent burning.", "Serve with rice or bread."],
        "tips": ["⚠️ Cut potatoes small (1cm cubes) — big pieces take forever on induction.",
                 "💡 Cover the pan — steam helps cook potatoes faster.",
                 "🥔 Don't stir too often — let them get crispy on each side."],
        "safetyNotes": ["Oil may splatter — keep lid nearby."],
        "calories": 260, "protein": 4, "carbs": 36, "fat": 12
    },

    # ---- KETTLE + INDUCTION / MULTI-APPLIANCE ----
    {
        "id": "h-17", "name": "Ramen Upgrade",
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600",
        "appliances": ["kettle", "induction"], "cookingTime": 12, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "medium", "tags": ["midnight-snack", "one-pot", "mess-alternative"],
        "category": "midnight-snack",
        "ingredients": [
            {"name": "Instant Ramen", "qty": "1 pack"}, {"name": "Egg", "qty": "1"},
            {"name": "Spring Onion", "qty": "1 (chopped)"}, {"name": "Soy Sauce", "qty": "1 tsp"},
            {"name": "Chili Flakes", "qty": "1/2 tsp"}
        ],
        "steps": ["Boil water in kettle.", "Cook noodles in a pot on induction with the boiling water.",
                  "Crack an egg into the simmering noodles.", "Add soy sauce and chili flakes.",
                  "Top with spring onions, serve."],
        "tips": ["💡 Don't stir the egg — let it poach in the broth for a runny yolk.",
                 "⚠️ Add seasoning packet first, then taste — you might not need all of it."],
        "safetyNotes": ["Standard kitchen safety applies."],
        "calories": 420, "protein": 14, "carbs": 50, "fat": 18
    },
    {
        "id": "h-18", "name": "Cheesy Bread Omelette",
        "image": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=600",
        "appliances": ["induction"], "cookingTime": 10, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "low", "tags": ["no-flame", "midnight-snack", "quick-fix"],
        "category": "midnight-snack",
        "ingredients": [
            {"name": "Egg", "qty": "2"}, {"name": "Bread", "qty": "2 slices"},
            {"name": "Cheese", "qty": "1 slice"}, {"name": "Onion", "qty": "1 tbsp chopped"},
            {"name": "Salt", "qty": "to taste"}, {"name": "Butter", "qty": "1 tsp"}
        ],
        "steps": ["Beat eggs with onion and salt.", "Heat butter in pan on medium.",
                  "Pour eggs, place bread slices on top.", "Flip when bottom sets.",
                  "Add cheese on top, fold, cook 1 more min.", "Serve hot."],
        "tips": ["💡 Place bread immediately after pouring eggs — it sticks together perfectly.",
                 "⚠️ Don't rush the flip — wait till the edges are firm."],
        "safetyNotes": ["Non-stick pan recommended for easy flipping."],
        "calories": 350, "protein": 20, "carbs": 26, "fat": 18
    },
    {
        "id": "h-19", "name": "Dalia (Broken Wheat Porridge)",
        "image": "https://images.unsplash.com/photo-1517673400267-0251440c45dc?w=600",
        "appliances": ["induction"], "cookingTime": 20, "difficulty": "Beginner", "servings": 2,
        "powerUsage": "medium", "tags": ["no-flame", "budget", "healthy-cheap", "one-pot"],
        "category": "healthy-cheap",
        "ingredients": [
            {"name": "Dalia (Broken Wheat)", "qty": "1/2 cup"}, {"name": "Water", "qty": "2 cups"},
            {"name": "Onion", "qty": "1 small"}, {"name": "Cumin Seeds", "qty": "1/2 tsp"},
            {"name": "Turmeric", "qty": "1/4 tsp"}, {"name": "Oil", "qty": "1 tbsp"},
            {"name": "Salt", "qty": "to taste"}
        ],
        "steps": ["Heat oil, add cumin seeds.", "Add onion, fry till golden.",
                  "Add dalia, roast 2 min.", "Add water, turmeric, salt.",
                  "Cook on low 15 min till soft.", "Serve with curd or pickle."],
        "tips": ["💡 Roasting dalia before adding water gives better flavor.",
                 "⚠️ It absorbs water — add more if needed for softer texture.",
                 "🥄 Stir occasionally to prevent sticking."],
        "safetyNotes": ["Let it cool slightly before eating — it retains heat."],
        "calories": 280, "protein": 10, "carbs": 44, "fat": 8
    },
    {
        "id": "h-20", "name": "Banana Milkshake",
        "image": "https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=600",
        "appliances": ["mixer"], "cookingTime": 3, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "low", "tags": ["budget", "healthy-cheap", "quick-fix"],
        "category": "healthy-cheap",
        "ingredients": [
            {"name": "Banana", "qty": "2 ripe"}, {"name": "Milk", "qty": "1 glass"},
            {"name": "Sugar/Honey", "qty": "1 tbsp"}, {"name": "Ice", "qty": "2-3 cubes (optional)"}
        ],
        "steps": ["Peel and break bananas into pieces.", "Add milk, sugar/honey, and ice to mixer jar.",
                  "Blend for 30-40 seconds.", "Pour into a glass and serve immediately."],
        "tips": ["💡 Ripe bananas (with brown spots) are sweeter — need less sugar.",
                 "⚠️ Don't blend too long — it becomes frothy and loses thickness."],
        "safetyNotes": ["Make sure mixer lid is on tight before blending."],
        "calories": 220, "protein": 6, "carbs": 40, "fat": 5
    },
    {
        "id": "h-21", "name": "Mango Lassi",
        "image": "https://images.unsplash.com/photo-1527585743534-7113e3211270?w=600",
        "appliances": ["mixer"], "cookingTime": 3, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "low", "tags": ["budget", "healthy-cheap", "quick-fix"],
        "category": "healthy-cheap",
        "ingredients": [
            {"name": "Mango Pulp", "qty": "1/2 cup"}, {"name": "Curd (Yogurt)", "qty": "1/2 cup"},
            {"name": "Milk", "qty": "1/2 cup"}, {"name": "Sugar", "qty": "1 tbsp"}
        ],
        "steps": ["Add all ingredients to mixer.", "Blend for 30 seconds till smooth.",
                  "Pour and serve cold."],
        "tips": ["💡 Frozen mango pulp makes it extra cold without watering it down with ice.",
                 "⚠️ Don't use sour curd — it makes the lassi taste off."],
        "safetyNotes": ["Standard mixer safety — ensure lid is secure."],
        "calories": 200, "protein": 6, "carbs": 36, "fat": 4
    },
    {
        "id": "h-22", "name": "Tomato Rice (Quick)",
        "image": "https://images.unsplash.com/photo-1596560548464-f010549b84d7?w=600",
        "appliances": ["induction"], "cookingTime": 25, "difficulty": "Beginner", "servings": 2,
        "powerUsage": "high", "tags": ["no-flame", "one-pot", "mess-alternative", "budget"],
        "category": "mess-alternative",
        "ingredients": [
            {"name": "Rice", "qty": "1 cup"}, {"name": "Tomato", "qty": "2 medium"},
            {"name": "Onion", "qty": "1 small"}, {"name": "Turmeric", "qty": "1/4 tsp"},
            {"name": "Oil", "qty": "1 tbsp"}, {"name": "Water", "qty": "2 cups"},
            {"name": "Salt", "qty": "to taste"}
        ],
        "steps": ["Heat oil, fry onion till golden.", "Add chopped tomatoes, cook till soft.",
                  "Add washed rice, turmeric, salt.", "Add water, bring to boil.",
                  "Reduce heat, cover, cook 18 min.", "Fluff with fork and serve."],
        "tips": ["⚠️ Don't open lid while rice is cooking — steam is important.",
                 "💡 Use 2:1 water-to-rice ratio for perfect texture.",
                 "🍅 Ripe red tomatoes give best flavor."],
        "safetyNotes": ["Hot steam when opening lid — always open away from face."],
        "calories": 350, "protein": 8, "carbs": 60, "fat": 8
    },
    {
        "id": "h-23", "name": "Masala Chai",
        "image": "https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=600",
        "appliances": ["induction"], "cookingTime": 8, "difficulty": "Beginner", "servings": 2,
        "powerUsage": "low", "tags": ["no-flame", "budget", "quick-fix"],
        "category": "lazy-cooking",
        "ingredients": [
            {"name": "Water", "qty": "1 cup"}, {"name": "Milk", "qty": "1 cup"},
            {"name": "Tea Leaves", "qty": "1.5 tsp"}, {"name": "Sugar", "qty": "2 tsp"},
            {"name": "Ginger", "qty": "1 small piece (crushed)"}
        ],
        "steps": ["Boil water with ginger on induction.", "Add tea leaves, boil 2 min.",
                  "Add milk and sugar.", "Let it boil up once, then reduce heat.",
                  "Strain into cups and serve."],
        "tips": ["💡 Crush ginger slightly — don't slice it — for stronger flavor.",
                 "⚠️ Watch when milk is added — it boils over very fast!",
                 "🫖 Boil tea leaves in water first, NOT milk — it extracts better."],
        "safetyNotes": ["Milk boils over quickly — never leave unattended."],
        "calories": 80, "protein": 3, "carbs": 12, "fat": 3
    },
    {
        "id": "h-24", "name": "Curd Rice",
        "image": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=600",
        "appliances": ["induction"], "cookingTime": 15, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "medium", "tags": ["no-flame", "budget", "healthy-cheap", "mess-alternative"],
        "category": "healthy-cheap",
        "ingredients": [
            {"name": "Cooked Rice", "qty": "1 cup (leftover)"}, {"name": "Curd (Yogurt)", "qty": "1/2 cup"},
            {"name": "Milk", "qty": "2 tbsp"}, {"name": "Salt", "qty": "to taste"},
            {"name": "Mustard Seeds", "qty": "1/4 tsp"}, {"name": "Curry Leaves", "qty": "3-4"},
            {"name": "Oil", "qty": "1 tsp"}
        ],
        "steps": ["Mash cooked rice slightly.", "Mix in curd, milk, and salt.",
                  "Heat oil, pop mustard seeds and curry leaves.", "Pour tempering over rice.",
                  "Mix well and serve cool."],
        "tips": ["💡 Best with leftover rice — it absorbs curd better.",
                 "⚠️ Don't add curd while rice is hot — it'll curdle.",
                 "🧂 Mix salt last — curd can vary in sourness."],
        "safetyNotes": ["Standard cooking precautions."],
        "calories": 250, "protein": 8, "carbs": 42, "fat": 6
    },
    {
        "id": "h-25", "name": "Peanut Butter Toast",
        "image": "https://images.unsplash.com/photo-1509722747041-616f39b57569?w=600",
        "appliances": ["kettle"], "cookingTime": 3, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "low", "tags": ["kettle-only", "no-flame", "budget", "healthy-cheap", "quick-fix"],
        "category": "lazy-cooking",
        "ingredients": [
            {"name": "Bread", "qty": "2 slices"}, {"name": "Peanut Butter", "qty": "2 tbsp"},
            {"name": "Banana", "qty": "1/2 (optional)"}, {"name": "Honey", "qty": "1 tsp (optional)"}
        ],
        "steps": ["No cooking needed!", "Spread peanut butter on bread.",
                  "Add sliced banana if available.", "Drizzle honey on top.", "Eat as-is."],
        "tips": ["💡 Toasting bread slightly makes peanut butter spread easier.",
                 "🍌 Banana adds sweetness — you can skip honey if using banana."],
        "safetyNotes": ["No safety concerns — it's a no-cook recipe!"],
        "calories": 320, "protein": 12, "carbs": 34, "fat": 16
    },
    {
        "id": "h-26", "name": "Chili Garlic Noodles",
        "image": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=600",
        "appliances": ["induction"], "cookingTime": 15, "difficulty": "Beginner", "servings": 2,
        "powerUsage": "medium", "tags": ["no-flame", "midnight-snack", "one-pot"],
        "category": "midnight-snack",
        "ingredients": [
            {"name": "Instant Noodles", "qty": "2 packs"}, {"name": "Garlic", "qty": "4 cloves (minced)"},
            {"name": "Soy Sauce", "qty": "1 tbsp"}, {"name": "Chili Sauce", "qty": "1 tbsp"},
            {"name": "Oil", "qty": "1 tbsp"}, {"name": "Spring Onion", "qty": "2 (chopped)"}
        ],
        "steps": ["Boil noodles on induction, drain, keep aside.", "Heat oil, fry garlic till golden.",
                  "Add soy sauce and chili sauce.", "Toss in noodles, mix well on high heat.",
                  "Garnish with spring onions, serve."],
        "tips": ["⚠️ Don't burn the garlic — it turns bitter. Cook only till golden.",
                 "💡 Drain noodles and toss with a tiny bit of oil to prevent clumping.",
                 "🔥 High heat tossing gives restaurant-style texture."],
        "safetyNotes": ["Garlic can pop in oil — add carefully."],
        "calories": 400, "protein": 10, "carbs": 54, "fat": 16
    },
    {
        "id": "h-27", "name": "Khichdi (Rice + Lentil Porridge)",
        "image": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=600",
        "appliances": ["induction"], "cookingTime": 25, "difficulty": "Beginner", "servings": 2,
        "powerUsage": "high", "tags": ["no-flame", "one-pot", "budget", "healthy-cheap"],
        "category": "healthy-cheap",
        "ingredients": [
            {"name": "Rice", "qty": "1/2 cup"}, {"name": "Moong Dal", "qty": "1/4 cup"},
            {"name": "Water", "qty": "3 cups"}, {"name": "Turmeric", "qty": "1/4 tsp"},
            {"name": "Ghee", "qty": "1 tsp"}, {"name": "Salt", "qty": "to taste"},
            {"name": "Cumin Seeds", "qty": "1/2 tsp"}
        ],
        "steps": ["Wash rice and dal together.", "Heat ghee, add cumin seeds.",
                  "Add rice, dal, water, turmeric, salt.", "Bring to boil, then simmer 20 min.",
                  "Stir till mushy. Serve with pickle or curd."],
        "tips": ["💡 More water = softer khichdi. Students prefer it mushy.",
                 "⚠️ Stir occasionally so it doesn't stick to the bottom.",
                 "🍚 This is the ultimate comfort food when you're sick."],
        "safetyNotes": ["Hot steam — open lid carefully."],
        "calories": 320, "protein": 12, "carbs": 54, "fat": 6
    },
    {
        "id": "h-28", "name": "Lemonade / Nimbu Pani",
        "image": "https://images.unsplash.com/photo-1621263764928-df1444c5e859?w=600",
        "appliances": [], "cookingTime": 3, "difficulty": "Beginner", "servings": 1,
        "powerUsage": "low", "tags": ["no-flame", "budget", "healthy-cheap", "quick-fix"],
        "category": "lazy-cooking",
        "ingredients": [
            {"name": "Lemon", "qty": "1"}, {"name": "Water", "qty": "1 glass"},
            {"name": "Sugar", "qty": "2 tsp"}, {"name": "Salt", "qty": "a pinch"},
            {"name": "Ice", "qty": "optional"}
        ],
        "steps": ["Squeeze lemon into a glass.", "Add sugar, salt, and cold water.",
                  "Stir well till sugar dissolves.", "Add ice if available. Enjoy."],
        "tips": ["💡 Add a pinch of roasted cumin powder for extra flavor.",
                 "🍋 Roll the lemon before squeezing — you get more juice."],
        "safetyNotes": ["No safety concerns — no cooking involved!"],
        "calories": 50, "protein": 0, "carbs": 14, "fat": 0
    },
    {
        "id": "h-29", "name": "Paneer Bhurji",
        "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600",
        "appliances": ["induction"], "cookingTime": 12, "difficulty": "Beginner", "servings": 2,
        "powerUsage": "medium", "tags": ["no-flame", "budget", "quick-fix"],
        "category": "quick-fix",
        "ingredients": [
            {"name": "Paneer", "qty": "200g (crumbled)"}, {"name": "Onion", "qty": "1 small"},
            {"name": "Tomato", "qty": "1 small"}, {"name": "Green Chili", "qty": "1"},
            {"name": "Turmeric", "qty": "1/4 tsp"}, {"name": "Oil", "qty": "1 tbsp"},
            {"name": "Salt", "qty": "to taste"}
        ],
        "steps": ["Heat oil, add chopped onions.", "Fry 2 min, add tomatoes and chili.",
                  "Cook till tomatoes soften.", "Add crumbled paneer and turmeric.",
                  "Toss for 3-4 minutes. Serve with bread."],
        "tips": ["💡 Crumble paneer with hands — irregular pieces taste better than cubes.",
                 "⚠️ Don't overcook paneer — it becomes rubbery.",
                 "🧅 Cook onions till slightly brown for better flavor."],
        "safetyNotes": ["Standard induction safety."],
        "calories": 320, "protein": 18, "carbs": 8, "fat": 24
    },
    {
        "id": "h-30", "name": "Aloo Paratha (Stuffed Bread)",
        "image": "https://images.unsplash.com/photo-1600289031464-74d374b64991?w=600",
        "appliances": ["induction"], "cookingTime": 25, "difficulty": "Intermediate", "servings": 2,
        "powerUsage": "medium", "tags": ["no-flame", "mess-alternative", "budget"],
        "category": "mess-alternative",
        "ingredients": [
            {"name": "Wheat Flour", "qty": "2 cups"}, {"name": "Potato", "qty": "2 boiled"},
            {"name": "Green Chili", "qty": "1"}, {"name": "Salt", "qty": "to taste"},
            {"name": "Oil/Ghee", "qty": "2 tbsp"}, {"name": "Water", "qty": "as needed"}
        ],
        "steps": ["Knead flour with water into soft dough. Rest 10 min.",
                  "Mash boiled potatoes with chili and salt.", "Make small dough balls, stuff with potato.",
                  "Roll out gently into flat circles.", "Cook on hot pan with ghee, both sides till golden.",
                  "Serve with curd or pickle."],
        "tips": ["⚠️ Roll gently — stuffed parathas can tear if pressed too hard.",
                 "💡 Use dry flour on the surface to prevent sticking while rolling.",
                 "🥔 Mash potatoes well — no lumps should remain.",
                 "🔥 Medium heat is key — high heat cooks outside but leaves inside raw."],
        "safetyNotes": ["Be careful with hot pan and ghee — it splatters."],
        "calories": 380, "protein": 10, "carbs": 52, "fat": 14
    },
]


# =========================================
# SAFETY TIPS DATABASE
# =========================================

SAFETY_TIPS = {
    "kettle": [
        "⚡ Always keep the kettle on a flat, dry surface.",
        "🔌 Unplug immediately after use to save power.",
        "💧 Never overfill — water expands when boiling.",
        "⚠️ Don't boil anything other than water (unless it's a multi-purpose kettle).",
        "🧹 Descale your kettle monthly with vinegar water.",
        "❌ Never open the lid while water is boiling.",
    ],
    "induction": [
        "⚡ Use only induction-compatible (magnetic bottom) cookware.",
        "🔌 Don't overload sockets — induction draws a lot of power.",
        "💧 Keep the surface dry — water + electricity = danger.",
        "⚠️ Don't place metal utensils on the surface when it's on.",
        "🧹 Clean after every use — spills can damage the plate.",
        "❌ Don't use if the glass surface is cracked.",
        "⏱️ Many hostels have power limits — avoid running induction during peak hours.",
    ],
    "mixer": [
        "⚡ Always secure the lid before starting.",
        "🔌 Don't run continuously for more than 30 seconds — let the motor cool.",
        "💧 Don't overfill — leave 1/3 space for blending action.",
        "⚠️ Never put your hand inside when it's plugged in.",
        "🧹 Wash immediately after use — dried food is hard to clean.",
    ],
    "general": [
        "🏠 Keep a fire extinguisher or wet towel nearby.",
        "🔌 Don't use multiple high-power appliances on the same socket/extension.",
        "💧 Keep water away from all electrical connections.",
        "📱 Keep emergency numbers saved — ambulance, hostel warden.",
        "🗑️ Dispose of cooking waste properly — don't block drains.",
        "🧼 Wash hands before and after cooking.",
    ],
}

# =========================================
# FOOD FRESHNESS GUIDE
# =========================================

FRESHNESS_GUIDE = [
    {
        "item": "Eggs",
        "howToCheck": "Place in water — fresh eggs sink, bad eggs float.",
        "signs": ["Foul sulfur smell when cracked", "Watery, runny whites", "Discolored yolk"],
        "shelfLife": "2-3 weeks (room temp), 4-5 weeks (fridge)",
        "warning": "Never eat an egg that smells bad — risk of salmonella."
    },
    {
        "item": "Milk",
        "howToCheck": "Smell it — sour smell means it's gone bad.",
        "signs": ["Sour/acidic smell", "Lumpy texture", "Yellowish color"],
        "shelfLife": "2-3 days after opening (fridge)",
        "warning": "Don't boil and re-refrigerate multiple times."
    },
    {
        "item": "Bread",
        "howToCheck": "Check for mold spots — green/white fuzzy patches.",
        "signs": ["Visible mold (any color)", "Stale, hard texture", "Sour smell"],
        "shelfLife": "3-5 days (room temp), 1-2 weeks (fridge)",
        "warning": "If one slice has mold, throw the whole loaf — mold spreads invisibly."
    },
    {
        "item": "Rice (cooked)",
        "howToCheck": "Smell it — sour smell means bacteria growth.",
        "signs": ["Sour smell", "Slimy texture", "Hard, dry grains"],
        "shelfLife": "1 day (room temp), 3-4 days (fridge)",
        "warning": "Reheated rice can cause food poisoning if not stored properly."
    },
    {
        "item": "Vegetables",
        "howToCheck": "Check texture and color — wilting and discoloration are signs.",
        "signs": ["Slimy surface", "Brown/black spots", "Soft, mushy texture", "Bad smell"],
        "shelfLife": "3-7 days depending on type (fridge)",
        "warning": "Cut away small bad spots — but if most is affected, throw it out."
    },
    {
        "item": "Paneer",
        "howToCheck": "Smell and touch — should be firm and mild-smelling.",
        "signs": ["Sour smell", "Slimy surface", "Yellowish edges"],
        "shelfLife": "2-3 days (fridge), 1 day (room temp)",
        "warning": "Keep submerged in water in the fridge to keep it fresh longer."
    },
]

# =========================================
# STORAGE TIPS
# =========================================

STORAGE_TIPS = [
    {"title": "Stack vertically", "tip": "Stand packets upright in a box — saves 30% more space than laying flat."},
    {"title": "Use zip-lock bags", "tip": "Transfer open packets into zip-locks to prevent spills and keep fresh."},
    {"title": "Under-bed storage", "tip": "Keep non-perishable items (noodles, oats, rice) in a box under your bed."},
    {"title": "Hanging organizer", "tip": "Use a shoe organizer on the back of your door for spice packets and small items."},
    {"title": "One-bowl system", "tip": "You only need: 1 bowl, 1 plate, 1 spoon, 1 fork, 1 mug. That's it."},
    {"title": "Keep essentials together", "tip": "Oil, salt, turmeric, chili powder — keep in a small tray that's always ready."},
    {"title": "Clean as you cook", "tip": "Wash your pan/bowl immediately — food sticks if left overnight."},
    {"title": "Airtight containers", "tip": "Small plastic containers keep rice, dal, and spices fresh for weeks."},
]


# =========================================
# SEARCH ENGINE
# =========================================

def search_hostel_recipes(
    ingredients: List[str],
    appliances: List[str],
    servings: int = 1,
    max_time: Optional[int] = None,
    tags: Optional[List[str]] = None,
    category: Optional[str] = None,
    limit: int = 5,
) -> List[Dict]:
    """
    Search hostel recipes by ingredients + appliances + filters.
    Returns scored, sorted results.
    """
    ingredients_lower = [i.lower().strip() for i in ingredients]
    appliances_lower = [a.lower().strip() for a in appliances]

    scored_recipes = []

    for recipe in HOSTEL_RECIPES:
        # STRICT: recipe appliances must be a subset of user's available appliances
        recipe_appliances = [a.lower() for a in recipe.get("appliances", [])]
        if recipe_appliances and not all(a in appliances_lower for a in recipe_appliances):
            continue

        # Time filter
        if max_time and recipe["cookingTime"] > max_time:
            continue

        # Tag filter
        if tags:
            recipe_tags = [t.lower() for t in recipe.get("tags", [])]
            if not any(t.lower() in recipe_tags for t in tags):
                continue

        # Category filter
        if category and recipe.get("category", "").lower() != category.lower():
            continue

        # SCORE: ingredient matching
        recipe_ingredients = [ing["name"].lower() for ing in recipe["ingredients"]]
        matched = sum(1 for ui in ingredients_lower
                      if any(ui in ri or ri in ui for ri in recipe_ingredients))
        total = len(recipe_ingredients)
        score = (matched / total * 100) if total > 0 else 0

        # Bonus for beginner
        if recipe["difficulty"] == "Beginner":
            score += 10
        # Bonus for fewer ingredients (simpler)
        if total <= 5:
            score += 5
        # Bonus for quick cooking
        if recipe["cookingTime"] <= 10:
            score += 5

        # Adjust servings
        adjusted = dict(recipe)
        if servings > 1 and recipe["servings"] == 1:
            for ing in adjusted["ingredients"]:
                ing = dict(ing)  # copy
            adjusted["servings"] = servings

        adjusted["matchedIngredients"] = matched
        adjusted["totalIngredients"] = total
        adjusted["score"] = round(score, 1)

        scored_recipes.append(adjusted)

    # Sort by score descending
    scored_recipes.sort(key=lambda r: r["score"], reverse=True)

    # Return top results (minimum 3 if possible)
    return scored_recipes[:max(limit, 3)]


def get_suggestions(category: Optional[str] = None, limit: int = 5) -> List[Dict]:
    """Get lifestyle-based recipe suggestions."""
    if category:
        results = [r for r in HOSTEL_RECIPES if r.get("category", "").lower() == category.lower()]
    else:
        results = list(HOSTEL_RECIPES)

    import random as _rand
    _rand.shuffle(results)
    return results[:limit]


def get_safety_tips(appliance: Optional[str] = None) -> Dict:
    """Get safety tips for specific or all appliances."""
    if appliance and appliance.lower() in SAFETY_TIPS:
        return {appliance.lower(): SAFETY_TIPS[appliance.lower()], "general": SAFETY_TIPS["general"]}
    return SAFETY_TIPS


def get_freshness_guide() -> List[Dict]:
    """Get food freshness detection guide."""
    return FRESHNESS_GUIDE


def get_storage_tips() -> List[Dict]:
    """Get storage and space optimization tips."""
    return STORAGE_TIPS
