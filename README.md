# 🍳 Prepzy – AI-Powered Recipe Planner

A modern, full-stack recipe recommendation application that matches your available ingredients to 250,000+ recipes across worldwide cuisines.

## ✨ Features

- **🔍 Smart Recipe Search** – Input ingredients and get AI-matched recipes with scoring
- **🎯 Preference Filters** – Filter by cooking time, skill level, cuisine, mood, and meal type
- **👨‍🍳 Step-by-Step Cooking Mode** – Full-screen guided cooking with timer and voice support
- **📊 Nutrition Tracking** – Calories, protein, carbs, and fat for every recipe
- **💬 AI Chatbot** – Get cooking tips, substitutions, and recipe suggestions
- **❤️ Favorites** – Save and organize your favorite recipes
- **🛒 Grocery List** – Auto-generate shopping lists from recipes
- **🌙 Dark/Light Mode** – Beautiful UI in both themes
- **🌍 Multi-Language** – English, Tamil, and German
- **📱 Fully Responsive** – Works on mobile, tablet, and desktop
- **📷 Image Recognition** – Upload ingredient photos (simulated AI detection)
- **🌤️ Mood & Weather Suggestions** – Get recommendations based on how you feel

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React.js + Vite + Tailwind CSS |
| **Backend** | Python FastAPI |
| **Animations** | Framer Motion |
| **Icons** | Lucide React |
| **Auth** | Local (Supabase-ready) |
| **Database** | In-memory + JSON (Supabase/MongoDB-ready) |

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- npm

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at **http://localhost:5173**

### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend API will be available at **http://localhost:8000**

## 📁 Project Structure

```
cooksy/
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   │   ├── Navbar.jsx
│   │   │   ├── ThemeToggle.jsx
│   │   │   ├── LanguageSwitcher.jsx
│   │   │   ├── IngredientInput.jsx
│   │   │   ├── PreferencesPanel.jsx
│   │   │   ├── RecipeCard.jsx
│   │   │   ├── FavoriteButton.jsx
│   │   │   ├── CookingMode.jsx
│   │   │   ├── Chatbot.jsx
│   │   │   └── LoadingSkeleton.jsx
│   │   ├── pages/           # Route pages
│   │   │   ├── Landing.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Signup.jsx
│   │   │   ├── Search.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── RecipePage.jsx
│   │   │   ├── Favorites.jsx
│   │   │   ├── GroceryPage.jsx
│   │   │   └── Profile.jsx
│   │   ├── context/         # React contexts
│   │   │   ├── AuthContext.jsx
│   │   │   ├── ThemeContext.jsx
│   │   │   ├── LanguageContext.jsx
│   │   │   └── FavoritesContext.jsx
│   │   ├── services/api.js  # Backend API layer
│   │   ├── data/            # Translations & recipes
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css        # Design system
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── recipes.py
│   │   │   ├── favorites.py
│   │   │   └── chatbot.py
│   │   ├── services/        # Business logic
│   │   │   ├── recipe_engine.py
│   │   │   ├── auth_service.py
│   │   │   └── chatbot_service.py
│   │   ├── models/schemas.py
│   │   └── main.py
│   └── requirements.txt
└── README.md
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/signup` | Create new user |
| POST | `/api/login` | Authenticate user |
| POST | `/api/search-recipes` | Search recipes by ingredients |
| GET | `/api/recipes/:id` | Get recipe details |
| POST | `/api/recommend` | Get personalized recommendations |
| POST | `/api/save-recipe` | Save to favorites |
| GET | `/api/get-favorites/:id` | Get user favorites |
| POST | `/api/chat` | Chat with AI assistant |

## 🎨 Design System

- **Colors**: Warm amber/orange primary, sage green accents, cream backgrounds
- **Dark Mode**: Deep charcoal with warm amber highlights
- **Typography**: Inter (body) + Playfair Display (headings) from Google Fonts
- **Components**: Glassmorphism cards, gradient buttons, animated chips
- **Animations**: Framer Motion for page transitions, card reveals, hover effects

## 🔮 Production Upgrades

To make this production-ready:

1. **Supabase Integration**: Add your Supabase URL and anon key to environment variables
2. **OpenAI API**: Connect chatbot to GPT for real AI responses
3. **MongoDB/PostgreSQL**: Migrate from in-memory to a real database
4. **250K Recipes**: Import a real recipe dataset (e.g., Recipe1M+)
5. **Image Recognition**: Integrate Google Cloud Vision or similar API
6. **PWA**: Add service worker for true offline support

## 📄 License

MIT License - Built with ❤️ by Prepzy Team
