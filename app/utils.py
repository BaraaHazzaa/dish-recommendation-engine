# app/utils.py

import pandas as pd
from sqlalchemy import text
import logging
from .models import engine, TOP_N

logger = logging.getLogger(__name__)

def extract_user_ratings(engine):
    """Extract user ratings from UserRating table by mapping CustomerID to UserID."""
    query = """
    SELECT 
        Customer.UserID, 
        UserRating.DishID, 
        UserRating.Rating
    FROM UserRating
    JOIN Customer ON UserRating.CustomerID = Customer.CustomerID
    WHERE UserRating.Rating IS NOT NULL
    """
    try:
        ratings = pd.read_sql(query, engine)
        logger.info("User ratings extracted successfully.")
        return ratings
    except Exception as e:
        logger.error(f"Error extracting user ratings: {e}")
        return pd.DataFrame()

def extract_user_orders(engine):
    """Extract user orders from Order and OrderItem tables by mapping CustomerID to UserID."""
    query = """
    SELECT 
        Customer.UserID, 
        OrderItem.DishID, 
        COUNT(*) AS PurchaseCount
    FROM "Order"
    JOIN OrderItem ON "Order".OrderID = OrderItem.OrderID
    JOIN Customer ON "Order".CustomerID = Customer.CustomerID
    WHERE "Order".Status = 'Completed'
    GROUP BY Customer.UserID, OrderItem.DishID
    """
    try:
        orders = pd.read_sql(query, engine)
        logger.info("User orders extracted successfully.")
        return orders
    except Exception as e:
        logger.error(f"Error extracting user orders: {e}")
        return pd.DataFrame()

def extract_dish_features(engine):
    """
    Extract dish features including categories, ingredients, and additional features like spiciness, 
    along with popularity based on order count and average rating.
    """
    query = """
    SELECT 
        Dish.DishID, 
        Dish.Name AS DishName, 
        Category.CategoryID, 
        Category.Name AS Category, 
        COALESCE(GROUP_CONCAT(DISTINCT Ingredient.Name), '') AS Ingredient, 
        COALESCE(GROUP_CONCAT(DISTINCT DishFeature.Name), '') AS Features, 
        COALESCE(COUNT(OrderItem.OrderID), 0) AS OrderCount,  -- Count of orders for popularity
        COALESCE(AVG(UserRating.Rating), 0) AS AverageRating  -- Average rating for popularity
    FROM Dish
    LEFT JOIN DishCategory ON Dish.DishID = DishCategory.DishID
    LEFT JOIN Category ON DishCategory.CategoryID = Category.CategoryID
    LEFT JOIN DishIngredient ON Dish.DishID = DishIngredient.DishID
    LEFT JOIN Ingredient ON DishIngredient.IngredientID = Ingredient.IngredientID
    LEFT JOIN OrderItem ON Dish.DishID = OrderItem.DishID
    LEFT JOIN UserRating ON Dish.DishID = UserRating.DishID
    LEFT JOIN DishFeatureMapping ON Dish.DishID = DishFeatureMapping.DishID
    LEFT JOIN DishFeature ON DishFeatureMapping.FeatureID = DishFeature.FeatureID
    GROUP BY Dish.DishID, Category.CategoryID, Category.Name
    """
    try:
        # Execute the query and retrieve the result as a pandas DataFrame
        dish_features = pd.read_sql(query, engine)

        # Calculate popularity based on order count and average rating
        dish_features['Popularity'] = dish_features['OrderCount'] + (dish_features['AverageRating'] * 2)

        logger.info("Dish features and popularity extracted successfully.")
        return dish_features

    except Exception as e:
        logger.error(f"Error extracting dish features: {e}")
        return pd.DataFrame()


def extract_user_preferences(engine):
    """Extract user preferences from UserPreference table."""
    query = """
    SELECT 
        UserID, 
        FavoriteDish, 
        DietaryRestrictions, 
        CategoryID, 
        PreferenceScore
    FROM UserPreference
    """
    try:
        preferences = pd.read_sql(query, engine)
        logger.info("User preferences extracted successfully.")
        return preferences
    except Exception as e:
        logger.error(f"Error extracting user preferences: {e}")
        return pd.DataFrame()

def preprocess_interaction_data(ratings, orders):
    """Combine ratings and orders into a unified user-item interaction matrix."""
    try:
        # Normalize PurchaseCount to a 1-5 scale to match ratings
        if not orders.empty:
            orders['NormalizedRating'] = orders['PurchaseCount'] / orders['PurchaseCount'].max() * 5
            orders_normalized = orders.rename(columns={'NormalizedRating': 'Rating'})
            combined_ratings = pd.concat([
                ratings[['UserID', 'DishID', 'Rating']], 
                orders_normalized[['UserID', 'DishID', 'Rating']]
            ], ignore_index=True)
        else:
            combined_ratings = ratings.copy()
        
        # Pivot to create User-Item Matrix
        user_item_matrix = combined_ratings.pivot_table(
            index='UserID', 
            columns='DishID', 
            values='Rating'
        ).fillna(0)
        logger.info("User-Item interaction matrix created.")
        return user_item_matrix
    except Exception as e:
        logger.error(f"Error in preprocessing interaction data: {e}")
        return pd.DataFrame()

def preprocess_dish_features(dish_features_df):
    """Aggregate dish features into a combined text field and apply weights as string concatenation."""
    try:
        # Handle missing values
        dish_features_df = dish_features_df.fillna('')

        # Aggregate features per Dish
        dish_features_agg = dish_features_df.groupby('DishID').agg({
            'DishName': 'first',
            'CategoryID': 'first',
            'Category': lambda x: ' '.join(x.unique()),
            'Ingredient': lambda x: ' '.join(x.unique()),
            'Features': lambda x: ' '.join(x.unique())
        }).reset_index()

        # Ensure all columns are strings before applying weights
        dish_features_agg['Category'] = dish_features_agg['Category'].astype(str)
        dish_features_agg['Ingredient'] = dish_features_agg['Ingredient'].astype(str)
        dish_features_agg['Features'] = dish_features_agg['Features'].astype(str)

        # Concatenate to create 'combined_features'
        dish_features_agg['combined_features'] = (
            dish_features_agg['DishName'] + ' ' +
            dish_features_agg['Category'] + ' ' +
            dish_features_agg['Ingredient'] + ' ' +
            dish_features_agg['Features']
        )

        # Add order count and average rating (if available) from OrderItem and UserRating tables
        dish_order_rating_query = """
        SELECT
            Dish.DishID,
            COALESCE(COUNT(OrderItem.OrderID), 0) AS OrderCount,
            COALESCE(AVG(UserRating.Rating), 0) AS AverageRating
        FROM Dish
        LEFT JOIN OrderItem ON Dish.DishID = OrderItem.DishID
        LEFT JOIN UserRating ON Dish.DishID = UserRating.DishID
        GROUP BY Dish.DishID
        """

        # Execute the query and retrieve order and rating data
        dish_order_rating = pd.read_sql(dish_order_rating_query, engine)

        # Merge the order count and rating into the aggregated dish features
        dish_features_agg = dish_features_agg.merge(dish_order_rating, on='DishID', how='left')

        # Calculate popularity based on order count and average rating
        dish_features_agg['Popularity'] = dish_features_agg['OrderCount'] + (dish_features_agg['AverageRating'] * 2)

        logger.info("Dish features preprocessed and aggregated successfully.")
        return dish_features_agg
    except Exception as e:
        logger.error(f"Error in preprocessing dish features: {e}")
        return pd.DataFrame()

def apply_business_rules(recommendations, user_id, preferences_df):
    """Apply business rules such as dietary restrictions, availability, and special promotions."""
    try:
        logger.info(f"Applying business rules for User ID {user_id}.")

        # Ensure the 'Reason' column exists in recommendations DataFrame
        if 'Reason' not in recommendations.columns:
            recommendations['Reason'] = ''  # Initialize with empty strings

        # Fetch user preferences
        user_prefs = preferences_df[preferences_df['UserID'] == user_id]

        # Dietary Restrictions
        dietary_restrictions_ids = user_prefs['DietaryRestrictions'].dropna().unique().tolist()
        if dietary_restrictions_ids:
            logger.info(f"Applying dietary restrictions: {dietary_restrictions_ids}")
            recommendations['Penalty'] = recommendations['Category'].apply(
                lambda x: 0.5 if x in dietary_restrictions_ids else 1.0
            )
            recommendations['Score'] *= recommendations['Penalty']
            recommendations = recommendations.drop(columns=['Penalty'])

        # Special Promotions
        current_date = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        special_query = """
        SELECT SpecialDishID FROM SpecialDish
        WHERE SpecialStartDate <= :current_date AND SpecialEndDate >= :current_date
        """
        with engine.connect() as connection:
            special_dishes = pd.read_sql(
                text(special_query),
                connection,
                params={'current_date': current_date}
            )

        if not special_dishes.empty:
            special_dish_ids = special_dishes['SpecialDishID'].tolist()
            logger.info(f"Applying special promotions for Dish IDs: {special_dish_ids}")
            recommendations.loc[recommendations['DishID'].isin(special_dish_ids), 'Score'] += 1
            recommendations['Reason'] = recommendations.apply(
                lambda row: 'Special Promotion' if row['DishID'] in special_dish_ids else row['Reason'], axis=1
            )

        # Inventory Constraints
        inventory_query = """
        SELECT Dish.DishID, SUM(Storage.Quantity) AS TotalQuantity
        FROM Dish
        JOIN DishIngredient ON Dish.DishID = DishIngredient.DishID
        JOIN Storage ON DishIngredient.IngredientID = Storage.IngredientID
        GROUP BY Dish.DishID
        """
        with engine.connect() as connection:
            available_dishes = pd.read_sql(
                text(inventory_query),
                connection
            )
        recommendations = recommendations.merge(available_dishes, on='DishID', how='left')
        recommendations['TotalQuantity'] = recommendations['TotalQuantity'].fillna(0)

        # Update availability status based on inventory
        recommendations['AvailabilityStatus'] = recommendations['TotalQuantity'].apply(
            lambda x: 'In Stock' if x > 0 else 'Out of Stock'
        )

        # Filter only dishes that are 'In Stock'
        recommendations = recommendations[recommendations['AvailabilityStatus'] == 'In Stock']

        # Penalize dishes with low inventory instead of excluding them
        low_stock_threshold = 5  # Set a threshold for low stock
        recommendations['InventoryPenalty'] = recommendations['TotalQuantity'].apply(
            lambda x: 0.5 if x < low_stock_threshold else 1.0
        )
        recommendations['Score'] *= recommendations['InventoryPenalty']
        recommendations = recommendations.drop(columns=['InventoryPenalty', 'TotalQuantity', 'AvailabilityStatus'])

        logger.info("Business rules applied to recommendations.")
        return recommendations
    except Exception as e:
        logger.error(f"Error applying business rules: {e}")
        return recommendations
