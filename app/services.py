import pandas as pd
import numpy as np
from sqlalchemy import text
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from .utils import (
    extract_user_ratings,
    extract_user_orders,
    extract_dish_features,
    extract_user_preferences,
    preprocess_interaction_data,
    preprocess_dish_features,
    apply_business_rules
)
from config.config import Config
from .models import engine, TOP_N

import logging

logger = logging.getLogger(__name__)

# Global dictionary to store models and related data
models = {}

def initialize_models():
    """
    Initialize and train Collaborative Filtering (CF) and Content-Based Filtering (CBF) models.
    This function should be called during application startup and whenever user data changes.
    """
    try:
        logger.info("Initializing recommendation models...")

        # Extract data from the database
        ratings = extract_user_ratings(engine)
        orders = extract_user_orders(engine)
        dish_features = extract_dish_features(engine)
        preferences = extract_user_preferences(engine)
        
        # Preprocess data
        user_item_matrix = preprocess_interaction_data(ratings, orders)
        dish_features_agg = preprocess_dish_features(dish_features)
        
        # Check if user_item_matrix is empty
        if user_item_matrix.empty:
            logger.warning("User-Item interaction matrix is empty. No data available for training.")
            return
        
        # Train Collaborative Filtering model
        svd, latent_matrix, item_factors = train_collaborative_filtering(user_item_matrix)
        
        # Train Content-Based Filtering model
        tfidf, content_similarity, feature_matrix = train_content_based(dish_features_agg)
        
        # Update the global models dictionary with the latest models and data
        models.clear()  # Clear existing models to avoid stale data
        models['user_item_matrix'] = user_item_matrix
        models['svd'] = svd
        models['latent_matrix'] = latent_matrix
        models['item_factors'] = item_factors
        models['tfidf'] = tfidf
        models['content_similarity'] = content_similarity
        models['feature_matrix'] = feature_matrix
        models['dish_features_agg'] = dish_features_agg
        models['preferences'] = preferences
        models['engine'] = engine  # Database engine
        
        logger.info("Recommendation models initialized successfully.")
    except Exception as e:
        logger.error(f"Error during model initialization: {e}")

def train_collaborative_filtering(user_item_matrix, n_components=50):
    """
    Train a Collaborative Filtering model using Truncated SVD.
    
    Parameters:
        user_item_matrix (pd.DataFrame): User-Item interaction matrix.
        n_components (int): Number of latent factors for SVD.
        
    Returns:
        tuple: (TruncatedSVD model, user latent factors, item latent factors)
    """
    try:
        logger.info("Training Collaborative Filtering model...")

        # Ensure n_components does not exceed the smaller dimension of the matrix
        n_components = min(n_components, min(user_item_matrix.shape) - 1)

        svd = TruncatedSVD(n_components=n_components, random_state=42)
        latent_matrix = svd.fit_transform(user_item_matrix)  # User latent factors
        item_factors = svd.components_.T  # Item latent factors

        logger.info("Collaborative Filtering model trained successfully.")
        return svd, latent_matrix, item_factors
    except Exception as e:
        logger.error(f"Error training Collaborative Filtering model: {e}")
        return None, None, None

def train_content_based(dish_features_agg):
    """
    Train a Content-Based Filtering model using TF-IDF vectorization.
    
    Parameters:
        dish_features_agg (pd.DataFrame): Aggregated dish features.
        
    Returns:
        tuple: (TF-IDF Vectorizer, Cosine similarity matrix, Feature matrix)
    """
    try:
        logger.info("Training Content-Based Filtering model...")
        tfidf = TfidfVectorizer(stop_words='english', max_df=0.8, min_df=2)  # Adjusted parameters for diversity
        feature_matrix = tfidf.fit_transform(dish_features_agg['combined_features'])
        content_similarity = cosine_similarity(feature_matrix)
        logger.info("Content-Based Filtering model trained successfully.")
        return tfidf, content_similarity, feature_matrix
    except Exception as e:
        logger.error(f"Error training Content-Based Filtering model: {e}")
        return None, None, None

def generate_and_store_recommendations(user_id):
    """
    Generate recommendations for a user and store them in the database.
    
    Parameters:
        user_id (int): The ID of the user for whom to generate recommendations.
        
    Returns:
        bool: True if recommendations were generated and stored successfully, False otherwise.
    """
    try:
        logger.info(f"Generating recommendations for User ID: {user_id}")

        # Initialize an empty DataFrame for recommendations
        recommendations = pd.DataFrame()

        # Check if user exists in the interaction matrix
        if user_id in models['user_item_matrix'].index:
            logger.info(f"User ID {user_id} found in the interaction matrix. Generating hybrid recommendations.")
            # Generate hybrid recommendations using CF and CBF
            recommendations = generate_hybrid_recommendations(user_id)
        else:
            logger.info(f"User ID {user_id} not found in the interaction matrix. Checking user preferences.")
            # Check if user has preferences
            user_prefs = models['preferences'][models['preferences']['UserID'] == user_id]
            if not user_prefs.empty:
                logger.info(f"User ID {user_id} has preferences. Generating content-based recommendations.")
                # Generate content-based recommendations based on preferences
                recommendations = generate_content_based_recommendations(user_id)
            else:
                # Handle missing preferences with a fallback
                logger.warning(f"User ID {user_id} has no interactions or preferences. Recommending popular dishes.")
                recommendations = recommend_popular_dishes(models['dish_features_agg'])
                if recommendations.empty:
                    logger.warning(f"Still no fallback recommendations found for User ID {user_id}.")
                    return False

        if recommendations.empty:
            logger.info(f"No recommendations generated for User ID {user_id}.")
            return False

        # Insert recommendations into the database
        insert_recommendations(user_id, recommendations)

        logger.info(f"Recommendations generated and stored for User ID {user_id}.")
        return True
    except Exception as e:
        logger.error(f"Error generating and storing recommendations for User ID {user_id}: {e}")
        return False
    
def calculate_dynamic_weights(user_id):
    """
    Calculate dynamic weights for CF and CBF based on user activity level.
    
    Parameters:
        user_id (int): The ID of the user.
        
    Returns:
        tuple: (alpha, beta) where alpha is the weight for CF and beta for CBF.
    """
    # Retrieve the number of interactions for the user (e.g., number of orders or ratings)
    user_interactions = models['user_item_matrix'].loc[user_id].sum()
    
    # Define thresholds for low and high activity levels
    low_activity_threshold = 5  # Example threshold for low activity
    high_activity_threshold = 20  # Example threshold for high activity
    
    # Set dynamic weights based on the user's activity level
    if user_interactions <= low_activity_threshold:
        # More weight for CBF for low-activity users (e.g., new users)
        alpha = 0.3
        beta = 0.7
    elif user_interactions >= high_activity_threshold:
        # More weight for CF for highly active users
        alpha = 0.7
        beta = 0.3
    else:
        # Gradually adjust weights between CF and CBF based on activity level
        activity_range = high_activity_threshold - low_activity_threshold
        alpha = 0.3 + (0.4 * ((user_interactions - low_activity_threshold) / activity_range))
        beta = 1 - alpha
    
    return alpha, beta

def generate_hybrid_recommendations(user_id):
    """
    Generate top N recommendations for a user using hybrid CF and CBF with strong diversity encouragement.
    
    Parameters:
        user_id (int): The ID of the user.
        
    Returns:
        pd.DataFrame: DataFrame containing top N recommended dishes.
    """
    try:
        logger.info(f"Generating hybrid recommendations for User ID {user_id} with strong diversity encouragement.")

        # Retrieve user index in the interaction matrix
        if user_id not in models['user_item_matrix'].index:
            logger.error(f"User ID {user_id} not found in the interaction matrix.")
            return pd.DataFrame()  # Return empty DataFrame if user not found

        user_idx = models['user_item_matrix'].index.get_loc(user_id)

        # Retrieve user latent factors for CF
        user_latent_factors = models['latent_matrix'][user_idx]

        # Retrieve item latent factors for CF
        item_factors = models['item_factors']

        # Compute predicted ratings (dot product of user and item latent factors for CF)
        predicted_ratings = np.dot(item_factors, user_latent_factors)

        # Create CF scores as a Series with DishID as index
        dish_ids_cf = models['user_item_matrix'].columns  # Dishes in CF model
        cf_scores = pd.Series(predicted_ratings, index=dish_ids_cf)

        # Content-Based Filtering (CBF) Scores
        user_purchased_dishes = models['user_item_matrix'].loc[user_id]
        purchased_dishes = user_purchased_dishes[user_purchased_dishes > 0].index.tolist()

        if not purchased_dishes:
            logger.warning(f"User ID {user_id} has no purchased dishes. Setting CBF scores to zeros.")
            cbf_scores = pd.Series(0, index=models['dish_features_agg']['DishID'])
        else:
            # Map purchased dishes to indices in dish_features_agg
            purchased_indices = models['dish_features_agg'][models['dish_features_agg']['DishID'].isin(purchased_dishes)].index.tolist()
            if not purchased_indices:
                logger.warning(f"No matching purchased dishes found in dish features. Setting CBF scores to zeros.")
                cbf_scores = pd.Series(0, index=models['dish_features_agg']['DishID'])
            else:
                # Use content similarity matrix to get CBF scores
                cbf_scores_array = models['content_similarity'][purchased_indices].mean(axis=0)
                # Create CBF scores as a Series with DishID as index
                dish_ids_cbf = models['dish_features_agg']['DishID']
                cbf_scores = pd.Series(cbf_scores_array, index=dish_ids_cbf)

        # Align CF and CBF scores based on DishID
        cf_scores = cf_scores.reindex(cbf_scores.index).fillna(0)
        cbf_scores = cbf_scores.fillna(0)

        # Calculate dynamic weights for the user based on interaction level
        alpha, beta = calculate_dynamic_weights(user_id)
        logger.info(f"Dynamic weights for User ID {user_id}: alpha (CF) = {alpha}, beta (CBF) = {beta}")

        # Combine CF and CBF scores with dynamic weights
        final_scores = alpha * cf_scores.values + beta * cbf_scores.values

        # Create Recommendations DataFrame
        recommendations = pd.DataFrame({
            'DishID': cbf_scores.index,
            'Score': final_scores
        })

        # Exclude already purchased dishes
        recommendations = recommendations[~recommendations['DishID'].isin(purchased_dishes)]

        # Merge with dish details
        recommendations = recommendations.merge(models['dish_features_agg'], on='DishID', how='left')

        # Ensure 'Popularity' exists and calculate it if missing
        if 'Popularity' not in recommendations.columns:
            logger.info("Calculating popularity based on order count and rating data.")
            recommendations['Popularity'] = recommendations['OrderCount'] + (recommendations['AverageRating'] * 2)

        # Cap popular dishes (exclude top 20% most popular dishes)
        popularity_threshold = recommendations['Popularity'].quantile(0.8)
        recommendations = recommendations[recommendations['Popularity'] < popularity_threshold]

        # Stronger penalty for popular dishes to encourage diversity
        def dish_is_popular(dish_id):
            popularity = recommendations.set_index('DishID').loc[dish_id, 'Popularity']
            return popularity > recommendations['Popularity'].quantile(0.6)

        recommendations['Penalty'] = recommendations['DishID'].apply(lambda x: 0.7 if dish_is_popular(x) else 1.0)
        recommendations['Score'] *= recommendations['Penalty']

        # Add a larger random factor to encourage diversity
        recommendations['Score'] += np.random.uniform(0, 0.3, size=recommendations.shape[0])

        # Apply Business Rules (e.g., dietary restrictions, promotions, inventory)
        recommendations = apply_business_rules(recommendations, user_id, models['preferences'])

        # Ensure category diversity
        categories = recommendations['Category'].value_counts()
        min_categories = 3  # Require at least 3 categories in the top results
        top_n_with_categories = pd.DataFrame()

        for category in categories.index:
            top_n_with_categories = pd.concat([
                top_n_with_categories,
                recommendations[recommendations['Category'] == category].head(2)  # Allow max 2 dishes per category
            ])
            if len(top_n_with_categories) >= TOP_N:
                break

        # Handle any NaN values in 'Score' column
        top_n_with_categories['Score'] = top_n_with_categories['Score'].fillna(0)

        # Get Top N Recommendations with category diversity
        top_n = top_n_with_categories.sort_values(by='Score', ascending=False).head(TOP_N)
        top_n['Reason'] = 'Hybrid Score with Dynamic Weights and Category Diversity'

        logger.info(f"Top {TOP_N} hybrid recommendations with dynamic weights generated for User ID {user_id}.")
        return top_n[['DishID', 'DishName', 'Category', 'Ingredient', 'Score', 'Reason']]
    except Exception as e:
        logger.error(f"Error generating hybrid recommendations for User ID {user_id}: {e}")
        return pd.DataFrame()

def generate_content_based_recommendations(user_id):
    """
    Generate top N recommendations for a user based on their preferences.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        pd.DataFrame: DataFrame containing top N recommended dishes.
    """
    try:
        logger.info(f"Generating content-based recommendations for User ID {user_id}.")

        # Fetch user preferences
        user_prefs = models['preferences'][models['preferences']['UserID'] == user_id]
        if user_prefs.empty:
            logger.warning(f"No preferences found for User ID {user_id}. Cannot generate content-based recommendations.")
            return pd.DataFrame()

        # Calculate weighted preferences
        user_prefs = user_prefs.copy()
        user_prefs['Weight'] = user_prefs['PreferenceScore'] / user_prefs['PreferenceScore'].sum()

        # Check for favorite dishes
        favorite_dishes = user_prefs['FavoriteDish'].dropna().unique().tolist()

        if not favorite_dishes:
            logger.info(f"User ID {user_id} has preferences but no favorite dishes. Using CategoryID for recommendations.")

            # Ensure 'CategoryID' exists in both user_prefs and dish_features_agg
            if 'CategoryID' not in models['dish_features_agg'].columns:
                logger.error("CategoryID column not found in dish features.")
                return pd.DataFrame()

            # Use CategoryID to recommend dishes
            category_ids = user_prefs['CategoryID'].dropna().unique().tolist()
            potential_dishes = models['dish_features_agg'][models['dish_features_agg']['CategoryID'].isin(category_ids)]

            # If no matches found, expand criteria to popular or related categories
            if potential_dishes.empty:
                logger.warning(f"No dishes found for the preferred categories for User ID {user_id}. Using popular dishes.")
                # Fallback to globally popular dishes if no category matches
                potential_dishes = recommend_popular_dishes(models['dish_features_agg'])

            if potential_dishes.empty:
                logger.warning(f"Still no recommendations found for User ID {user_id} even after fallback.")
                return pd.DataFrame()

            # Calculate scores based on CategoryID
            scores_by_category = user_prefs.groupby('CategoryID')['Weight'].sum()
            potential_dishes['Score'] = potential_dishes['CategoryID'].map(scores_by_category)

            # Handle NaN values in 'Score' column
            potential_dishes['Score'] = potential_dishes['Score'].fillna(0)

            # Remove dishes with zero score if necessary
            potential_dishes = potential_dishes[potential_dishes['Score'] > 0]

            # Apply Business Rules
            recommendations = apply_business_rules(potential_dishes, user_id, models['preferences'])

            # Get Top N Recommendations
            recommendations = recommendations.sort_values(by='Score', ascending=False).head(TOP_N)
            recommendations['Reason'] = 'Category-Based Preference'

        else:
            # Handle favorite dishes logic if present
            favorite_indices = models['dish_features_agg'][models['dish_features_agg']['DishID'].isin(favorite_dishes)].index.tolist()
            if not favorite_indices:
                logger.warning(f"No matching favorite dishes found for User ID {user_id}.")
                return pd.DataFrame()

            # Compute content similarity based recommendations
            weighted_content = np.zeros(models['content_similarity'].shape[1])
            for idx, row in user_prefs.iterrows():
                if pd.notnull(row['FavoriteDish']):
                    dish_id = row['FavoriteDish']
                    dish_entry = models['dish_features_agg'][models['dish_features_agg']['DishID'] == dish_id]
                    if not dish_entry.empty:
                        dish_idx = dish_entry.index[0]
                        weighted_content += row['Weight'] * models['content_similarity'][dish_idx]

            cbf_scores = weighted_content

            # Handle any NaN values
            cbf_scores = np.nan_to_num(cbf_scores)

            # Create Recommendations DataFrame
            recommendations = pd.DataFrame({
                'DishID': models['dish_features_agg']['DishID'],
                'Score': cbf_scores
            })

            # Merge with dish details
            recommendations = recommendations.merge(models['dish_features_agg'], on='DishID', how='left')

            # Apply Business Rules
            recommendations = apply_business_rules(recommendations, user_id, models['preferences'])

            # Handle any NaN values in 'Score' column
            recommendations['Score'] = recommendations['Score'].fillna(0)

            # Get Top N Recommendations
            recommendations = recommendations.sort_values(by='Score', ascending=False).head(TOP_N)
            recommendations['Reason'] = 'Preference-Based'

        logger.info(f"Top {TOP_N} content-based recommendations generated for User ID {user_id}.")
        return recommendations[['DishID', 'DishName', 'Category', 'Ingredient', 'Score', 'Reason']]
    except Exception as e:
        logger.error(f"Error generating content-based recommendations for User ID {user_id}: {e}")
        return pd.DataFrame()

def recommend_popular_dishes(dish_features_agg):
    """
    Fallback to globally popular dishes when specific preferences cannot be matched.

    Parameters:
        dish_features_agg (pd.DataFrame): Aggregated dish features.

    Returns:
        pd.DataFrame: DataFrame containing popular dishes.
    """
    try:
        # If a 'Popularity' column does not exist, calculate popularity based on available data
        if 'Popularity' not in dish_features_agg.columns:
            logger.info("Calculating popularity based on available data (e.g., orders, ratings).")
            # Example of creating a popularity score: combining ratings and orders
            dish_features_agg['Popularity'] = (
                dish_features_agg.get('RatingCount', 0) +  # Assumes a column 'RatingCount' exists
                dish_features_agg.get('OrderCount', 0)    # Assumes a column 'OrderCount' exists
            )

        # Handle any NaN values in 'Popularity' column
        dish_features_agg['Popularity'] = dish_features_agg['Popularity'].fillna(0)

        # Sort by the calculated popularity score
        popular_dishes = dish_features_agg.sort_values(by='Popularity', ascending=False).head(TOP_N)

        # Add a 'Score' column to match the expected schema
        popular_dishes['Score'] = popular_dishes['Popularity']  # Use popularity as the score

        # Set the 'Reason' for recommendations
        popular_dishes['Reason'] = 'Popular Dish'

        logger.info("Recommended popular dishes as fallback.")
        return popular_dishes[['DishID', 'DishName', 'Category', 'Ingredient', 'Score', 'Reason']]
    except Exception as e:
        logger.error(f"Error generating popular dish recommendations: {e}")
        return pd.DataFrame()

def insert_recommendations(user_id, recommendations_df):
    """
    Insert generated recommendations into the DishRecommendation table after clearing old ones.
    
    Parameters:
        user_id (int): The ID of the user.
        recommendations_df (pd.DataFrame): DataFrame containing recommendations.
    """
    try:
        if recommendations_df.empty:
            logger.info(f"No recommendations to insert for User ID {user_id}.")
            return

        logger.info(f"Clearing old recommendations for User ID {user_id}.")

        # Delete old recommendations for the user
        delete_query = """
        DELETE FROM DishRecommendation WHERE UserID = :user_id
        """
        with engine.connect() as connection:
            connection.execute(text(delete_query), {'user_id': user_id})
        
        logger.info(f"Old recommendations cleared for User ID {user_id}.")

        logger.info(f"Inserting new recommendations for User ID {user_id} into the database.")
        
        # Ensure the 'Score' and 'Reason' fields exist in the DataFrame
        if 'Score' not in recommendations_df.columns:
            recommendations_df['Score'] = 0  # Set a default score if missing
        if 'Reason' not in recommendations_df.columns:
            recommendations_df['Reason'] = 'Popular Dish'  # Set a default reason if missing

        # Prepare records for insertion
        records = recommendations_df.to_dict(orient='records')
        insert_query = """
        INSERT OR REPLACE INTO DishRecommendation (UserID, DishID, Reason, Score)
        VALUES (:UserID, :DishID, :Reason, :Score)
        """

        # Use a transaction context manager to handle commit and rollback automatically
        with engine.begin() as connection:  # Automatically starts a transaction
            try:
                for record in records:
                    connection.execute(
                        text(insert_query),
                        {
                            'UserID': user_id,
                            'DishID': record['DishID'],
                            'Reason': record.get('Reason', 'Popular Dish'),
                            'Score': record.get('Score', 0)
                        }
                    )
                logger.info(f"Recommendations inserted successfully for User ID {user_id}.")
            except Exception as e:
                logger.error(f"Error inserting recommendations for User ID {user_id}: {e}")
                raise  # The transaction will be rolled back automatically

    except Exception as e:
        logger.error(f"Failed to insert recommendations for User ID {user_id}: {e}")


def get_user_recommendations(user_id):
    """
    Retrieve stored recommendations for a user from the database.
    
    Parameters:
        user_id (int): The ID of the user.
        
    Returns:
        pd.DataFrame: DataFrame containing the user's recommendations.
    """
    try:
        logger.info(f"Retrieving recommendations for User ID {user_id}.")

        query = """
        SELECT Dish.DishID, Dish.Name AS Name, Dish.Description, Dish.Price, Dish.ImageURL, 
               DishRecommendation.Reason, DishRecommendation.Score, SUM(Storage.Quantity) AS TotalQuantity
        FROM DishRecommendation
        JOIN Dish ON DishRecommendation.DishID = Dish.DishID
        LEFT JOIN DishIngredient ON Dish.DishID = DishIngredient.DishID
        LEFT JOIN Storage ON DishIngredient.IngredientID = Storage.IngredientID
        WHERE DishRecommendation.UserID = :user_id
        GROUP BY Dish.DishID
        HAVING COALESCE(SUM(Storage.Quantity), 0) > 0
        ORDER BY DishRecommendation.Score DESC
        LIMIT :top_n
        """
        with engine.connect() as connection:
            recommendations = pd.read_sql(
                text(query),
                connection,
                params={'user_id': user_id, 'top_n': TOP_N}
            )
        
        if recommendations.empty:
            logger.info(f"No recommendations found for User ID {user_id}.")
            return recommendations
        
        logger.info(f"Recommendations retrieved successfully for User ID {user_id}.")
        return recommendations
    except Exception as e:
        logger.error(f"Error retrieving recommendations for User ID {user_id}: {e}")
        return pd.DataFrame()

def save_user_preferences(user_id, preferences):
    """
    Save user preferences to the database and generate recommendations.
    
    Parameters:
        user_id (int): The ID of the user.
        preferences (dict): A dictionary containing user preferences.
    """
    try:
        query = """
        INSERT INTO UserPreference (UserID, FavoriteDish, DietaryRestrictions, CategoryID, PreferenceScore)
        VALUES (:user_id, :favorite_dish, :dietary_restrictions, :category_id, :preference_score)
        ON CONFLICT (UserID) DO UPDATE SET
            FavoriteDish = EXCLUDED.FavoriteDish,
            DietaryRestrictions = EXCLUDED.DietaryRestrictions,
            CategoryID = EXCLUDED.CategoryID,
            PreferenceScore = EXCLUDED.PreferenceScore
        """
        with engine.connect() as connection:
            connection.execute(
                text(query),
                {
                    'user_id': user_id,
                    'favorite_dish': preferences.get('FavoriteDish'),
                    'dietary_restrictions': preferences.get('DietaryRestrictions'),
                    'category_id': preferences.get('CategoryID'),
                    'preference_score': preferences.get('PreferenceScore')
                }
            )
        
        # Re-initialize the models to reflect updated preferences
        initialize_models()  # Retrain models with updated data
        
        # Generate new recommendations with updated models
        generate_and_store_recommendations(user_id)
        
        logger.info(f"Preferences saved and recommendations generated for User ID {user_id}.")
    except Exception as e:
        logger.error(f"Error saving preferences for User ID {user_id}: {e}")

def save_user_ratings(user_id, ratings):
    """
    Save user ratings to the database and retrain models.
    
    Parameters:
        user_id (int): The ID of the user.
        ratings (list of dict): A list containing rating data.
    """
    try:
        # Insert or update user ratings in the database
        # (Assuming you have appropriate SQL queries to handle this)
        
        # **Re-initialize the models to reflect updated ratings**
        initialize_models()  # Retrain models with updated data
        
        # Generate new recommendations with updated models
        generate_and_store_recommendations(user_id)
        
        logger.info(f"Ratings saved and recommendations generated for User ID {user_id}.")
    except Exception as e:
        logger.error(f"Error saving ratings for User ID {user_id}: {e}")
