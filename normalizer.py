"""
Ingredient Normalizer
Cleans, normalizes, and standardizes ingredient strings for accurate matching.
Handles plurals, adjective modifiers, and common variations.
"""

import re
from typing import List


# ── Adjective / prep words to strip ──────────────────────────────────────────
_MODIFIERS = {
    "chopped", "diced", "sliced", "minced", "ground", "grated", "shredded",
    "crushed", "dried", "frozen", "canned", "cooked", "raw", "fresh",
    "roasted", "boiled", "steamed", "fried", "baked", "grilled", "smoked",
    "peeled", "deseeded", "halved", "quartered", "cubed", "julienned",
    "blanched", "sauteed", "sautéed", "melted", "softened", "chilled",
    "warm", "hot", "cold", "large", "medium", "small", "thin", "thick",
    "fine", "coarse", "extra", "whole", "boneless", "skinless",
    "unsalted", "salted", "low-fat", "fat-free", "organic",
}

# ── Explicit plural → singular overrides ─────────────────────────────────────
_PLURAL_MAP = {
    "tomatoes": "tomato",
    "potatoes": "potato",
    "onions": "onion",
    "mangoes": "mango",
    "avocados": "avocado",
    "carrots": "carrot",
    "peppers": "pepper",
    "mushrooms": "mushroom",
    "lemons": "lemon",
    "limes": "lime",
    "oranges": "orange",
    "apples": "apple",
    "bananas": "banana",
    "strawberries": "strawberry",
    "blueberries": "blueberry",
    "raspberries": "raspberry",
    "cherries": "cherry",
    "peaches": "peach",
    "grapes": "grape",
    "olives": "olive",
    "cloves": "clove",
    "leaves": "leaf",
    "eggs": "egg",
    "beans": "bean",
    "peas": "pea",
    "nuts": "nut",
    "seeds": "seed",
    "shrimps": "shrimp",
    "prawns": "prawn",
    "noodles": "noodle",
    "tortillas": "tortilla",
    "almonds": "almond",
    "walnuts": "walnut",
    "cashews": "cashew",
    "peanuts": "peanut",
    "pecans": "pecan",
    "lentils": "lentil",
    "chickpeas": "chickpea",
    "sprouts": "sprout",
}

# ── Common synonym / alias map ───────────────────────────────────────────────
_SYNONYMS = {
    "capsicum": "bell pepper",
    "coriander leaves": "cilantro",
    "coriander": "cilantro",
    "spring onion": "green onion",
    "scallion": "green onion",
    "chilli": "chili",
    "chillies": "chili",
    "chilies": "chili",
    "chilis": "chili",
    "aubergine": "eggplant",
    "courgette": "zucchini",
    "rocket": "arugula",
    "curd": "yogurt",
    "dahi": "yogurt",
    "maize": "corn",
    "groundnut": "peanut",
    "groundnuts": "peanut",
    "lady finger": "okra",
    "ladyfinger": "okra",
    "bhindi": "okra",
}


def normalize_ingredient(text: str) -> str:
    """
    Normalize a single ingredient string.

    Pipeline:
      1. Lowercase + strip
      2. Remove quantities / measurements  (e.g. "2 cups", "1/2 tsp")
      3. Remove parenthesised notes          (e.g. "(about 100g)")
      4. Strip modifier adjectives            (chopped, fresh …)
      5. Apply synonym map
      6. Singularize via explicit map + heuristic
      7. Collapse whitespace + final trim

    >>> normalize_ingredient("  2 cups Chopped Tomatoes  ")
    'tomato'
    >>> normalize_ingredient("fresh coriander leaves")
    'cilantro'
    """
    if not text:
        return ""

    t = text.lower().strip()

    # Remove parenthesised notes
    t = re.sub(r"\([^)]*\)", "", t)

    # Remove leading quantities  ("2", "1/2", "2.5", etc.) and units
    t = re.sub(
        r"^\s*[\d\./]+\s*"
        r"(cups?|tbsps?|tablespoons?|tsps?|teaspoons?|oz|ounces?"
        r"|lbs?|pounds?|grams?|g|kg|ml|liters?|litres?|pieces?|inch|cm|pinch)?\s*",
        "",
        t,
    )

    # Strip modifier words
    words = t.split()
    words = [w for w in words if w not in _MODIFIERS]
    t = " ".join(words)

    # Apply synonyms (check multi-word first, then single-word)
    if t in _SYNONYMS:
        t = _SYNONYMS[t]
    else:
        # Check if any multi-word synonym prefix matches
        for syn_key, syn_val in _SYNONYMS.items():
            if t == syn_key:
                t = syn_val
                break

    # Singularize — explicit map
    if t in _PLURAL_MAP:
        t = _PLURAL_MAP[t]
    else:
        # Heuristic singularization for simple words
        single_words = t.split()
        processed = []
        for w in single_words:
            if w in _PLURAL_MAP:
                processed.append(_PLURAL_MAP[w])
            elif len(w) > 3 and w.endswith("ies"):
                processed.append(w[:-3] + "y")  # berries → berry
            elif len(w) > 3 and w.endswith("ves"):
                processed.append(w[:-3] + "f")  # halves → half
            elif len(w) > 3 and w.endswith("es") and w not in {"cheese", "sauce", "rice", "juice", "spice"}:
                processed.append(w[:-2] if w[-3] in "sxzh" else w[:-1])
            elif len(w) > 3 and w.endswith("s") and w not in {"hummus", "couscous", "molasses", "asparagus", "citrus"}:
                processed.append(w[:-1])
            else:
                processed.append(w)
        t = " ".join(processed)

    # Collapse whitespace
    t = re.sub(r"\s+", " ", t).strip()
    return t


def normalize_list(ingredients: List[str]) -> List[str]:
    """
    Normalize a list of ingredient strings.
    Filters out empty results after normalization.
    """
    result = []
    for item in ingredients:
        normalized = normalize_ingredient(item)
        if normalized:
            result.append(normalized)
    return result
