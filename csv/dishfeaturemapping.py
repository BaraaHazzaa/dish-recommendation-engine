import pandas as pd
import os
import random

# Define dishes and features based on your provided data
dishes = list(range(1, 51))  # Dish IDs from 1 to 50
features = list(range(1, 10))  # Feature IDs from 1 to 9 (Spiciness, Saltiness, ...)

# Define the range of feature values for different types of dishes
feature_values = {
    "spicy_dishes": {"Spiciness": (7, 10), "Sweetness": (0, 2), "Creaminess": (3, 6)},
    "sweet_dishes": {"Spiciness": (0, 1), "Sweetness": (7, 10), "Creaminess": (4, 7)},
    "creamy_dishes": {"Spiciness": (0, 3), "Sweetness": (3, 6), "Creaminess": (7, 10)},
    "neutral_dishes": {"Spiciness": (0, 3), "Sweetness": (0, 4), "Creaminess": (0, 4)},
    # Add more categories as needed
}

# A dictionary to assign dish types
dish_type_map = {
    1: "neutral_dishes",
    2: "spicy_dishes",
    3: "creamy_dishes",
    4: "neutral_dishes",
    5: "spicy_dishes",
    6: "creamy_dishes",
    7: "neutral_dishes",
    8: "neutral_dishes",
    9: "neutral_dishes",
    10: "creamy_dishes",
    11: "spicy_dishes",
    12: "neutral_dishes",
    13: "neutral_dishes",
    14: "neutral_dishes",
    15: "neutral_dishes",
    16: "neutral_dishes",
    17: "neutral_dishes",
    18: "creamy_dishes",
    19: "neutral_dishes",
    20: "creamy_dishes",
    21: "neutral_dishes",
    22: "creamy_dishes",
    23: "neutral_dishes",
    24: "creamy_dishes",
    25: "neutral_dishes",
    26: "neutral_dishes",
    27: "neutral_dishes",
    28: "sweet_dishes",
    29: "sweet_dishes",
    30: "sweet_dishes",
    31: "sweet_dishes",
    32: "sweet_dishes",
    33: "neutral_dishes",
    34: "sweet_dishes",
    35: "sweet_dishes",
    36: "sweet_dishes",
    37: "neutral_dishes",
    38: "neutral_dishes",
    39: "neutral_dishes",
    40: "neutral_dishes",
    41: "neutral_dishes",
    42: "neutral_dishes",
    43: "neutral_dishes",
    44: "neutral_dishes",
    45: "spicy_dishes",
    46: "creamy_dishes",
    47: "spicy_dishes",
    48: "neutral_dishes",
    49: "neutral_dishes",
    50: "spicy_dishes",
}

# Generate DishFeatureMapping
dish_feature_mapping = []

for dish_id in dishes:
    dish_type = dish_type_map.get(dish_id, "neutral_dishes")
    for feature_id in features:
        feature_name = ["Spiciness", "Saltiness", "Sweetness", "Sourness", "Bitterness", "Umami", "Crunchiness", "Creaminess", "Juiciness"][feature_id - 1]
        if feature_name in feature_values[dish_type]:
            value_range = feature_values[dish_type][feature_name]
            feature_value = random.uniform(*value_range)
        else:
            feature_value = random.uniform(0, 2)  # Minimal contribution if not specified
        dish_feature_mapping.append({
            "DishID": dish_id,
            "FeatureID": feature_id,
            "FeatureValue": round(feature_value, 1)  # Rounded for simplicity
        })

# Convert to DataFrame
dish_feature_mapping_df = pd.DataFrame(dish_feature_mapping)

# Specify the directory where you want to save the file
output_directory = 'C:/Users/ASUS/Desktop/project-root 9-9 3/recommendation_service'
output_file = os.path.join(output_directory, 'dish_feature_mapping.csv')

# Check and create the directory if it does not exist
os.makedirs(output_directory, exist_ok=True)

# Save the DataFrame to a CSV file
dish_feature_mapping_df.to_csv(output_file, index=False)

print(f"DishFeatureMapping data has been successfully saved to {output_file}")
print("Current Working Directory:", os.getcwd())
