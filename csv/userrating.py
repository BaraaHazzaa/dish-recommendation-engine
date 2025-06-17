import pandas as pd
import random
import os

# Define user ratings data
user_ratings = []

# Adjust the range to reflect your actual 1000 customers
user_ids = range(1, 1001)  # User IDs from 1 to 1000

# Available dishes (from your dish data)
dish_ids = list(range(1, 51))  # Dish IDs from 1 to 50

# Generate user ratings data for 1000 users
rating_id = 1
for user_id in user_ids:
    # Each user rates a random number of dishes (between 5 and 15)
    rated_dishes = random.sample(dish_ids, random.randint(5, 15))
    for dish_id in rated_dishes:
        rating = random.randint(1, 5)  # Ratings from 1 to 5
        review_text = {
            1: "Terrible, not recommended.",
            2: "Not great, wouldn't order again.",
            3: "It was okay, nothing special.",
            4: "Quite good, I enjoyed it.",
            5: "Fantastic, highly recommend!"
        }[rating]  # Simple review text based on the rating
        
        # Build rating record
        user_ratings.append({
            "UserRatingID": rating_id,
            "CustomerID": user_id,
            "DishID": dish_id,
            "Rating": rating,
            "ReviewText": review_text
        })
        rating_id += 1

# Convert to DataFrame
user_ratings_df = pd.DataFrame(user_ratings)

# Specify the directory where you want to save the file
output_directory = 'C:/Users/ASUS/Desktop/project-root 9-9 3/recommendation_service'
output_file = os.path.join(output_directory, 'user_ratings.csv')

# Check and create the directory if it does not exist
os.makedirs(output_directory, exist_ok=True)

# Save the DataFrame to a CSV file
user_ratings_df.to_csv(output_file, index=False)

print(f"UserRatings data has been successfully saved to {output_file}")
print("Current Working Directory:", os.getcwd())
