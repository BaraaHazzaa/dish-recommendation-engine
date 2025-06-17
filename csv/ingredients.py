import pandas as pd
import os

# Updated and refined categories list
categories = [
    {"CategoryID": 1, "Name": "Main Course"},
    {"CategoryID": 2, "Name": "Appetizer"},
    {"CategoryID": 3, "Name": "Salad"},
    {"CategoryID": 4, "Name": "Soup"},
    {"CategoryID": 5, "Name": "Dessert"},
    {"CategoryID": 6, "Name": "Breakfast"},
    {"CategoryID": 7, "Name": "Sandwich"},
    {"CategoryID": 8, "Name": "Dinner"},
    {"CategoryID": 9, "Name": "Lunch"},
    {"CategoryID": 10, "Name": "Brunch"},
    {"CategoryID": 11, "Name": "Snacks"},
    {"CategoryID": 12, "Name": "American"},
    {"CategoryID": 13, "Name": "Italian"},
    {"CategoryID": 14, "Name": "Mexican"},
    {"CategoryID": 15, "Name": "French"},
    {"CategoryID": 16, "Name": "Indian"},
    {"CategoryID": 17, "Name": "Thai"},
    {"CategoryID": 18, "Name": "Vegetarian"},
    {"CategoryID": 19, "Name": "Vegan"},
    {"CategoryID": 20, "Name": "Gluten-Free"},
    {"CategoryID": 21, "Name": "Nut Allergy"},
    {"CategoryID": 22, "Name": "Lactose Intolerant"},
    {"CategoryID": 23, "Name": "Keto"},
    {"CategoryID": 24, "Name": "Paleo"},
    {"CategoryID": 25, "Name": "Low Sodium"},
    {"CategoryID": 26, "Name": "Sweet"},
    {"CategoryID": 27, "Name": "Savory"},
    {"CategoryID": 28, "Name": "Bitter"},
    {"CategoryID": 29, "Name": "Crispy/Crunchy"},
    {"CategoryID": 30, "Name": "Creamy"},
    {"CategoryID": 31, "Name": "Moist/Juicy"},
    {"CategoryID": 32, "Name": "Spicy"},
    {"CategoryID": 33, "Name": "Mild"},
    {"CategoryID": 34, "Name": "Medium"},
    {"CategoryID": 35, "Name": "Hot"}
]

# Convert the categories list to a DataFrame
categories_df = pd.DataFrame(categories)

# Specify the directory where you want to save the file
output_directory = 'C:/Users/ASUS/Desktop/project-root 9-9 3/recommendation_service'
output_file = os.path.join(output_directory, 'categories.csv')

# Check and create the directory if it does not exist
os.makedirs(output_directory, exist_ok=True)

# Save the DataFrame to a CSV file
categories_df.to_csv(output_file, index=False)

print(f"Categories data has been successfully saved to {output_file}")
print("Current Working Directory:", os.getcwd())
