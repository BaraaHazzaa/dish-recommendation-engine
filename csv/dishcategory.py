import pandas as pd
import os

# DishCategory mappings based on dishes and updated categories
dish_category = [
    {"DishID": 1, "CategoryID": 13}, # Margherita Pizzaaaaw - Italian
    {"DishID": 1, "CategoryID": 1},  # Main Course
    {"DishID": 2, "CategoryID": 13}, # Pepperoni Pizza - Italian
    {"DishID": 2, "CategoryID": 1},  # Main Course
    {"DishID": 3, "CategoryID": 13}, # Chicken Alfredo Pasta - Italian
    {"DishID": 3, "CategoryID": 1},  # Main Course
    {"DishID": 4, "CategoryID": 13}, # Spaghetti Bolognese - Italian
    {"DishID": 4, "CategoryID": 1},  # Main Course
    {"DishID": 5, "CategoryID": 14}, # Beef Tacos - Mexican
    {"DishID": 5, "CategoryID": 1},  # Main Course
    {"DishID": 6, "CategoryID": 14}, # Chicken Quesadilla - Mexican
    {"DishID": 6, "CategoryID": 1},  # Main Course
    {"DishID": 7, "CategoryID": 3},  # Caesar Salad
    {"DishID": 7, "CategoryID": 2},  # Appetizer
    {"DishID": 8, "CategoryID": 3},  # Greek Salad
    {"DishID": 8, "CategoryID": 2},  # Appetizer
    {"DishID": 9, "CategoryID": 4},  # French Onion Soup
    {"DishID": 9, "CategoryID": 15}, # French
    {"DishID": 10, "CategoryID": 4}, # Clam Chowder
    {"DishID": 10, "CategoryID": 30}, # Creamy
    {"DishID": 11, "CategoryID": 32}, # Buffalo Wings - Spicy
    {"DishID": 11, "CategoryID": 2},  # Appetizer
    {"DishID": 12, "CategoryID": 2},  # Mozzarella Sticks - Appetizer
    {"DishID": 12, "CategoryID": 29}, # Crispy/Crunchy
    {"DishID": 13, "CategoryID": 12}, # Cheeseburger - American
    {"DishID": 13, "CategoryID": 1},  # Main Course
    {"DishID": 14, "CategoryID": 12}, # Bacon Cheeseburger - American
    {"DishID": 14, "CategoryID": 1},  # Main Course
    {"DishID": 15, "CategoryID": 2},  # Chicken Tenders - Appetizer
    {"DishID": 15, "CategoryID": 12}, # American
    {"DishID": 15, "CategoryID": 29}, # Crispy/Crunchy
    {"DishID": 16, "CategoryID": 12}, # BBQ Ribs - American
    {"DishID": 16, "CategoryID": 1},  # Main Course
    {"DishID": 16, "CategoryID": 27}, # Savory
    {"DishID": 17, "CategoryID": 8},  # Grilled Salmon - Seafood
    {"DishID": 17, "CategoryID": 1},  # Main Course
    {"DishID": 17, "CategoryID": 31}, # Moist/Juicy
    {"DishID": 18, "CategoryID": 8},  # Shrimp Scampi - Seafood
    {"DishID": 18, "CategoryID": 1},  # Main Course
    {"DishID": 18, "CategoryID": 30}, # Creamy
    {"DishID": 19, "CategoryID": 8},  # Fish and Chips - Seafood
    {"DishID": 19, "CategoryID": 1},  # Main Course
    {"DishID": 19, "CategoryID": 29}, # Crispy/Crunchy
    {"DishID": 20, "CategoryID": 4},  # Lobster Bisque
    {"DishID": 20, "CategoryID": 8},  # Seafood
    {"DishID": 20, "CategoryID": 30}, # Creamy
    {"DishID": 21, "CategoryID": 12}, # Chicken Parmesan
    {"DishID": 21, "CategoryID": 1},  # Main Course
    {"DishID": 22, "CategoryID": 13}, # Lasagna - Italian
    {"DishID": 22, "CategoryID": 1},  # Main Course
    {"DishID": 23, "CategoryID": 13}, # Eggplant Parmesan - Italian
    {"DishID": 23, "CategoryID": 1},  # Main Course
    {"DishID": 23, "CategoryID": 18}, # Vegetarian
    {"DishID": 24, "CategoryID": 13}, # Ravioli - Italian
    {"DishID": 24, "CategoryID": 1},  # Main Course
    {"DishID": 25, "CategoryID": 2},  # Bruschetta - Appetizer
    {"DishID": 25, "CategoryID": 13}, # Italian
    {"DishID": 25, "CategoryID": 27}, # Savory
    {"DishID": 26, "CategoryID": 2},  # Fried Calamari - Appetizer
    {"DishID": 26, "CategoryID": 8},  # Seafood
    {"DishID": 26, "CategoryID": 29}, # Crispy/Crunchy
    {"DishID": 27, "CategoryID": 2},  # Garlic Bread - Appetizer
    {"DishID": 27, "CategoryID": 13}, # Italian
    {"DishID": 27, "CategoryID": 27}, # Savory
    {"DishID": 28, "CategoryID": 5},  # Chocolate Cake - Dessert
    {"DishID": 28, "CategoryID": 26}, # Sweet
    {"DishID": 29, "CategoryID": 5},  # Tiramisu - Dessert
    {"DishID": 29, "CategoryID": 13}, # Italian
    {"DishID": 29, "CategoryID": 26}, # Sweet
    {"DishID": 30, "CategoryID": 5},  # Cheesecake - Dessert
    {"DishID": 30, "CategoryID": 26}, # Sweet
    {"DishID": 30, "CategoryID": 30}, # Creamy
    {"DishID": 31, "CategoryID": 5},  # Apple Pie - Dessert
    {"DishID": 31, "CategoryID": 26}, # Sweet
    {"DishID": 32, "CategoryID": 6},  # Pancakes - Breakfast
    {"DishID": 32, "CategoryID": 26}, # Sweet
    {"DishID": 33, "CategoryID": 6},  # Omelette - Breakfast
    {"DishID": 33, "CategoryID": 30}, # Creamy
    {"DishID": 34, "CategoryID": 6},  # French Toast - Breakfast
    {"DishID": 34, "CategoryID": 26}, # Sweet
    {"DishID": 35, "CategoryID": 6},  # Eggs Benedict - Breakfast
    {"DishID": 35, "CategoryID": 30}, # Creamy
    {"DishID": 36, "CategoryID": 6},  # Waffles - Breakfast
    {"DishID": 36, "CategoryID": 26}, # Sweet
    {"DishID": 37, "CategoryID": 3},  # Cobb Salad
    {"DishID": 37, "CategoryID": 27}, # Savory
    {"DishID": 38, "CategoryID": 11}, # Club Sandwich
    {"DishID": 38, "CategoryID": 27}, # Savory
    {"DishID": 39, "CategoryID": 11}, # BLT Sandwich
    {"DishID": 39, "CategoryID": 27}, # Savory
    {"DishID": 40, "CategoryID": 11}, # Turkey Avocado Wrap
    {"DishID": 40, "CategoryID": 31}, # Moist/Juicy
    {"DishID": 41, "CategoryID": 15}, # Steak Frites - French
    {"DishID": 41, "CategoryID": 1},  # Main Course
    {"DishID": 41, "CategoryID": 31}, # Moist/Juicy
    {"DishID": 42, "CategoryID": 15}, # Coq au Vin - French
    {"DishID": 42, "CategoryID": 1},  # Main Course
    {"DishID": 43, "CategoryID": 15}, # Ratatouille - French
    {"DishID": 43, "CategoryID": 1},  # Main Course
    {"DishID": 43, "CategoryID": 18}, # Vegetarian
    {"DishID": 44, "CategoryID": 15}, # Beef Bourguignon - French
    {"DishID": 44, "CategoryID": 1},  # Main Course
    {"DishID": 44, "CategoryID": 27}, # Savory
    {"DishID": 45, "CategoryID": 16}, # Chicken Curry - Indian
    {"DishID": 45, "CategoryID": 32}, # Spicy
    {"DishID": 46, "CategoryID": 16}, # Butter Chicken - Indian
    {"DishID": 46, "CategoryID": 1},  # Main Course
    {"DishID": 46, "CategoryID": 30}, # Creamy
    {"DishID": 47, "CategoryID": 16}, # Lamb Rogan Josh - Indian
    {"DishID": 47, "CategoryID": 1},  # Main Course
    {"DishID": 47, "CategoryID": 32}, # Spicy
    {"DishID": 48, "CategoryID": 16}, # Vegetable Biryani - Indian
    {"DishID": 48, "CategoryID": 18}, # Vegetarian
    {"DishID": 49, "CategoryID": 17}, # Pad Thai - Thai
    {"DishID": 49, "CategoryID": 1},  # Main Course
    {"DishID": 50, "CategoryID": 17}, # Green Curry - Thai
    {"DishID": 50, "CategoryID": 32}, # Spicy
]

# Convert the data to a DataFrame
dish_category_df = pd.DataFrame(dish_category)

# Specify the directory where you want to save the file
output_directory = 'C:/Users/ASUS/Desktop/project-root 9-9 3/recommendation_service'
output_file = os.path.join(output_directory, 'dish_categories.csv')

# Check and create the directory if it does not exist
os.makedirs(output_directory, exist_ok=True)

# Save the DataFrame to a CSV file
dish_category_df.to_csv(output_file, index=False)

print(f"DishCategory data has been successfully saved to {output_file}")
print("Current Working Directory:", os.getcwd())
