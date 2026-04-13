"""
Chatbot service with keyword-based responses.
Replace with OpenAI API integration for production.
"""


def get_response(message: str) -> str:
    lower = message.lower()
    
    if any(w in lower for w in ['recipe', 'cook', 'make', 'suggest']):
        return "I can help you find recipes! Try telling me what ingredients you have, and I'll suggest something delicious. You can also use the Search page to find recipes by ingredients."
    
    if any(w in lower for w in ['substitute', 'replace', 'instead', 'alternative']):
        return ("Common substitutions:\n"
                "• Butter → Coconut oil or ghee\n"
                "• Eggs → Flax eggs (1 tbsp ground flax + 3 tbsp water)\n"
                "• Milk → Oat milk, almond milk, or coconut milk\n"
                "• Sugar → Honey, maple syrup, or jaggery\n"
                "• Cream → Coconut cream or cashew cream\n"
                "• All-purpose flour → Whole wheat flour or almond flour")
    
    if any(w in lower for w in ['quick', 'fast', 'time', 'minute', 'easy']):
        return ("Quick meals under 15 minutes:\n"
                "• Pasta Aglio e Olio 🍝\n"
                "• Egg Fried Rice 🍚\n"
                "• Avocado Toast 🥑\n"
                "• Sweet Corn Soup 🌽\n"
                "• Smoothie Bowl 🫐\n"
                "Try the Search page with 'Under 15 min' filter!")
    
    if any(w in lower for w in ['healthy', 'diet', 'weight', 'calorie', 'low', 'nutrition']):
        return ("Healthy meal recommendations:\n"
                "• Quinoa Buddha Bowl - 380 cal, high protein\n"
                "• Greek Salad - 220 cal, fresh & light\n"
                "• Miso Soup - 60 cal, warming\n"
                "• Oats Porridge - 260 cal, filling\n"
                "• Idli - 120 cal, steamed & light\n"
                "Use the 'Light & Healthy' mood filter for more options!")
    
    if any(w in lower for w in ['spicy', 'hot', 'chili', 'spice']):
        return ("Love spice? Try these:\n"
                "• Thai Green Curry 🌶️🌶️\n"
                "• Chole Bhature 🌶️\n"
                "• Chili Paneer 🌶️🌶️\n"
                "• Manchurian 🌶️\n"
                "• Pad Thai 🌶️")
    
    if any(w in lower for w in ['sweet', 'dessert', 'cake', 'sugar']):
        return ("Sweet tooth? Here are my picks:\n"
                "• Tiramisu - Italian classic ☕\n"
                "• Gulab Jamun - Indian sweet 🍯\n"
                "• Chocolate Lava Cake - Rich & decadent 🍫\n"
                "• Mango Lassi - Refreshing drink 🥭")
    
    if any(w in lower for w in ['hello', 'hi', 'hey', 'good']):
        return "Hello! 👋 I'm Prepzy Chef, your AI cooking assistant. Ask me about recipes, ingredient substitutions, healthy options, or anything food-related!"
    
    if any(w in lower for w in ['thank', 'thanks']):
        return "You're welcome! Happy cooking! 🍳✨ Feel free to ask anything else."
    
    return ("I'm your cooking assistant! I can help with:\n"
            "🍳 Recipe suggestions\n"
            "🔄 Ingredient substitutions\n"
            "⏱️ Quick meal ideas\n"
            "🥗 Healthy options\n"
            "🌶️ Cuisine recommendations\n\n"
            "Just ask me anything about cooking!")
