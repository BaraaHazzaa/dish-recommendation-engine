import pandas as pd
import random
import os

# Define user preferences data
user_preferences = []

# Correct range for your actual 1000 customers
user_ids = range(1, 1001)  # User IDs from 1 to 1000

# Available dishes (from your dish data)
dishes = [
    {"DishID": 1, "Name": "Margherita Pizzaaaaw", "Categories": [13, 1]},
    {"DishID": 2, "Name": "Pepperoni Pizza", "Categories": [13, 1]},
    {"DishID": 3, "Name": "Chicken Alfredo Pasta", "Categories": [13, 1]},
    {"DishID": 4, "Name": "Spaghetti Bolognese", "Categories": [13, 1]},
    {"DishID": 5, "Name": "Beef Tacos", "Categories": [14, 1]},
    {"DishID": 6, "Name": "Chicken Quesadilla", "Categories": [14, 1]},
    {"DishID": 7, "Name": "Caesar Salad", "Categories": [3, 2]},
    {"DishID": 8, "Name": "Greek Salad", "Categories": [3, 2]},
    {"DishID": 9, "Name": "French Onion Soup", "Categories": [4, 15]},
    {"DishID": 10, "Name": "Clam Chowder", "Categories": [4, 30]},
    {"DishID": 11, "Name": "Buffalo Wings", "Categories": [32, 2]},
    {"DishID": 12, "Name": "Mozzarella Sticks", "Categories": [2, 29]},
    {"DishID": 13, "Name": "Cheeseburger", "Categories": [12, 1]},
    {"DishID": 14, "Name": "Bacon Cheeseburger", "Categories": [12, 1]},
    {"DishID": 15, "Name": "Chicken Tenders", "Categories": [2, 12, 29]},
    {"DishID": 16, "Name": "BBQ Ribs", "Categories": [12, 1, 27]},
    {"DishID": 17, "Name": "Grilled Salmon", "Categories": [8, 1, 31]},
    {"DishID": 18, "Name": "Shrimp Scampi", "Categories": [8, 1, 30]},
    {"DishID": 19, "Name": "Fish and Chips", "Categories": [8, 1, 29]},
    {"DishID": 20, "Name": "Lobster Bisque", "Categories": [4, 8, 30]},
    {"DishID": 21, "Name": "Chicken Parmesan", "Categories": [12, 1]},
    {"DishID": 22, "Name": "Lasagna", "Categories": [13, 1]},
    {"DishID": 23, "Name": "Eggplant Parmesan", "Categories": [13, 1, 18]},
    {"DishID": 24, "Name": "Ravioli", "Categories": [13, 1]},
    {"DishID": 25, "Name": "Bruschetta", "Categories": [2, 13, 27]},
    {"DishID": 26, "Name": "Fried Calamari", "Categories": [2, 8, 29]},
    {"DishID": 27, "Name": "Garlic Bread", "Categories": [2, 13, 27]},
    {"DishID": 28, "Name": "Chocolate Cake", "Categories": [5, 26]},
    {"DishID": 29, "Name": "Tiramisu", "Categories": [5, 13, 26]},
    {"DishID": 30, "Name": "Cheesecake", "Categories": [5, 26, 30]},
    {"DishID": 31, "Name": "Apple Pie", "Categories": [5, 26]},
    {"DishID": 32, "Name": "Pancakes", "Categories": [6, 26]},
    {"DishID": 33, "Name": "Omelette", "Categories": [6, 30]},
    {"DishID": 34, "Name": "French Toast", "Categories": [6, 26]},
    {"DishID": 35, "Name": "Eggs Benedict", "Categories": [6, 30]},
    {"DishID": 36, "Name": "Waffles", "Categories": [6, 26]},
    {"DishID": 37, "Name": "Cobb Salad", "Categories": [3, 27]},
    {"DishID": 38, "Name": "Club Sandwich", "Categories": [11, 27]},
    {"DishID": 39, "Name": "BLT Sandwich", "Categories": [11, 27]},
    {"DishID": 40, "Name": "Turkey Avocado Wrap", "Categories": [11, 31]},
    {"DishID": 41, "Name": "Steak Frites", "Categories": [15, 1, 31]},
    {"DishID": 42, "Name": "Coq au Vin", "Categories": [15, 1]},
    {"DishID": 43, "Name": "Ratatouille", "Categories": [15, 1, 18]},
    {"DishID": 44, "Name": "Beef Bourguignon", "Categories": [15, 1, 27]},
    {"DishID": 45, "Name": "Chicken Curry", "Categories": [16, 32]},
    {"DishID": 46, "Name": "Butter Chicken", "Categories": [16, 1, 30]},
    {"DishID": 47, "Name": "Lamb Rogan Josh", "Categories": [16, 1, 32]},
    {"DishID": 48, "Name": "Vegetable Biryani", "Categories": [16, 18]},
    {"DishID": 49, "Name": "Pad Thai", "Categories": [17, 1]},
    {"DishID": 50, "Name": "Green Curry", "Categories": [17, 32]},
]

# Define possible dietary restrictions
dietary_restrictions = [18, 19, 20, 21, 22]  # Vegetarian, Vegan, Gluten-Free, Nut Allergy, Lactose Intolerant

# Generate user preferences data for 1000 users
preference_id = 1
for user_id in user_ids:
    # Generate a few preferences for each user
    for _ in range(random.randint(3, 6)):
        # Select a favorite dish and ensure categories align with user's restrictions
        favorite_dish = random.choice(dishes)
        dietary_choice = random.choice(dietary_restrictions) if random.random() > 0.5 else None
        
        # Ensure favorite dishes don't conflict with dietary restrictions
        if dietary_choice == 18:  # Vegetarian
            while 18 not in favorite_dish["Categories"]:
                favorite_dish = random.choice(dishes)
        elif dietary_choice == 19:  # Vegan
            while 18 not in favorite_dish["Categories"]:  # Assuming vegan is a subset of vegetarian in simplicity
                favorite_dish = random.choice(dishes)

        # Build preference record
        user_preferences.append({
            "PreferenceID": preference_id,
            "UserID": user_id,
            "FavoriteDish": favorite_dish["DishID"] if random.random() > 0.3 else None,
            "DietaryRestrictions": dietary_choice,
            "CategoryID": random.choice(favorite_dish["Categories"]),
            "PreferenceScore": random.randint(7, 10)  # Scores 7 to 10 for stronger preferences
        })
        preference_id += 1

# Convert to DataFrame
user_preferences_df = pd.DataFrame(user_preferences)

# Specify the directory where you want to save the file
output_directory = 'C:/Users/ASUS/Desktop/project-root 9-9 3/recommendation_service'
output_file = os.path.join(output_directory, 'user_preferences.csv')

# Check and create the directory if it does not exist
os.makedirs(output_directory, exist_ok=True)

# Save the DataFrame to a CSV file
user_preferences_df.to_csv(output_file, index=False)

print(f"UserPreferences data has been successfully saved to {output_file}")
print("Current Working Directory:", os.getcwd())
