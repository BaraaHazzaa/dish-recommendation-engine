# Dish Recommendation Engine

A machine learning-powered dish recommendation system that combines collaborative filtering (Truncated SVD) and content-based filtering (TF-IDF) to deliver personalized dish suggestions for a food service platform.

## Features
- **Hybrid Recommendations**: Combines user interaction data (ratings, orders) with dish features (categories, ingredients, etc.).
- **Dynamic Weighting**: Adjusts model influence based on user activity levels.
- **Business Rules**: Incorporates dietary restrictions, promotions, and inventory constraints.
- **Scalability**: Retrains models every 10 minutes using APScheduler for fresh recommendations.

├── categories.csv           # Category data
├── dishes.csv               # Dish data
├── dish_categories.csv      # Dish-to-category mappings
├── dish_feature_mapping.csv # Dish feature mappings
├── user_preferences.csv     # User preference data
├── user_ratings.csv         # User rating data
├── run.py                   # Application entry point
├── app/
│   ├── models.py            # Database models and engine
│   ├── routes.py            # API endpoints
│   ├── services.py          # Recommendation logic
│   ├── utils.py             # Data extraction and preprocessing
│   ├── init.py          # Python package initializer
├── config/
│   ├── config.py            # Configuration settings
├── csv/
│   ├── dishcategory.py      # Dish category processing
│   ├── dishes.py            # Dish data processing
│   ├── dishfeaturemapping.py# Dish feature processing
│   ├── ingredients.py       # Ingredient data processing
│   ├── userpreference.py    # User preference processing
│   ├── userrating.py        # User rating processing


## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/BaraaHazzaa/dish-recommendation-engine.git
2. Install dependencies:
    pip install -r requirements.txt

3. Configure the database in config/config.py (e.g., set DATABASE_URL).

4. Run the application:
    python run.py


#Technologies:

Python, Pandas, NumPy, Scikit-learn, SQLAlchemy
Flask (API routes)
APScheduler (periodic model retraining)
SQLite/PostgreSQL (database)

#Usage:

Access recommendations via API endpoints in routes.py.
Update preferences or ratings to trigger model retraining.
