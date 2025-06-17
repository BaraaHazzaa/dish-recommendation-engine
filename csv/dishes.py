import pandas as pd
import os

# Provided dishes data
dishes = [
    {"DishID": 1, "Name": "Margherita Pizza", "Description": "Classic pizza with tomato sauce mozzarella and basila", "Price": 10.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 2, "Name": "Pepperoni Pizza", "Description": "Pizza topped with pepperoni slices", "Price": 12.99, "AvailabilityStatus": "Out of Stock", "ImageURL": ""},
    {"DishID": 3, "Name": "Chicken Alfredo Pasta", "Description": "Creamy Alfredo sauce with grilled chicken and fettuccine pasta", "Price": 14.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 4, "Name": "Spaghetti Bolognese", "Description": "Traditional Italian pasta with meat sauce", "Price": 13.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 5, "Name": "Beef Tacos", "Description": "Soft tacos filled with seasoned beef lettuce and cheese", "Price": 9.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 6, "Name": "Chicken Quesadilla", "Description": "Grilled tortilla filled with chicken and cheese", "Price": 11.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 7, "Name": "Caesar Salad", "Description": "Fresh romaine lettuce with Caesar dressing croutons and Parmesan cheese", "Price": 8.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 8, "Name": "Greek Salad", "Description": "Salad with cucumbers tomatoes olives feta cheese and oregano", "Price": 7.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 9, "Name": "French Onion Soup", "Description": "Rich beef broth with caramelized onions and melted cheese", "Price": 6.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 10, "Name": "Clam Chowder", "Description": "Creamy soup with clams potatoes and celery", "Price": 8.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 11, "Name": "Buffalo Wings", "Description": "Spicy chicken wings served with blue cheese dressing", "Price": 9.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 12, "Name": "Mozzarella Sticks", "Description": "Breaded and fried mozzarella cheese served with marinara sauce", "Price": 7.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 13, "Name": "Cheeseburger", "Description": "Grilled beef patty with cheese lettuce tomato and pickles", "Price": 10.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 14, "Name": "Bacon Cheeseburger", "Description": "Grilled beef patty with cheese bacon lettuce tomato and pickles", "Price": 12.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 15, "Name": "Chicken Tenders", "Description": "Breaded and fried chicken tenders served with honey mustard", "Price": 9.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 16, "Name": "BBQ Ribs", "Description": "Slow cooked ribs with barbecue sauce", "Price": 16.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 17, "Name": "Grilled Salmon", "Description": "Grilled salmon fillet with lemon butter sauce", "Price": 18.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 18, "Name": "Shrimp Scampi", "Description": "Shrimp cooked in garlic butter sauce served over linguine.", "Price": 17.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 19, "Name": "Fish and Chips", "Description": "Battered and fried fish fillet served with French fries", "Price": 14.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 20, "Name": "Lobster Bisque", "Description": "Creamy lobster soup with a touch of sherry", "Price": 9.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 21, "Name": "Chicken Parmesan", "Description": "Breaded chicken breast topped with marinara sauce and mozzarella cheese", "Price": 15.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 22, "Name": "Lasagna", "Description": "Layers of pasta meat sauce and cheese baked to perfection", "Price": 14.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 23, "Name": "Eggplant Parmesan", "Description": "Breaded eggplant slices topped with marinara sauce and mozzarella cheese", "Price": 13.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 24, "Name": "Ravioli", "Description": "Pasta stuffed with ricotta cheese and spinach served with marinara sauce", "Price": 12.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 25, "Name": "Bruschetta", "Description": "Toasted bread topped with tomatoes garlic and basil", "Price": 6.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 26, "Name": "Fried Calamari", "Description": "Breaded and fried squid rings served with marinara sauce", "Price": 9.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 27, "Name": "Garlic Bread", "Description": "Toasted bread with garlic butter", "Price": 4.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 28, "Name": "Chocolate Cake", "Description": "Rich and moist chocolate cake with chocolate frosting", "Price": 6.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 29, "Name": "Tiramisu", "Description": "Classic Italian dessert with layers of coffee soaked ladyfingers and mascarpone cheese", "Price": 7.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 30, "Name": "Cheesecake", "Description": "Creamy cheesecake with a graham cracker crust", "Price": 6.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 31, "Name": "Apple Pie", "Description": "Traditional apple pie with a flaky crust", "Price": 5.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 32, "Name": "Pancakes", "Description": "Fluffy pancakes served with maple syrup", "Price": 5.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 33, "Name": "Omelette", "Description": "Classic omelette with cheese and vegetables", "Price": 6.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 34, "Name": "French Toast", "Description": "Bread dipped in egg batter and fried served with syrup", "Price": 6.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 35, "Name": "Eggs Benedict", "Description": "Poached eggs on English muffins with hollandaise sauce", "Price": 8.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 36, "Name": "Waffles", "Description": "Crisp waffles served with whipped cream and berries", "Price": 6.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 37, "Name": "Cobb Salad", "Description": "Salad with chicken bacon avocado eggs and blue cheese", "Price": 10.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 38, "Name": "Club Sandwich", "Description": "Triple decker sandwich with turkey bacon lettuce and tomato.", "Price": 9.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 39, "Name": "BLT Sandwich", "Description": "Sandwich with bacon lettuce and tomato", "Price": 7.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 40, "Name": "Turkey Avocado Wrap", "Description": "Wrap with turkey avocado lettuce and tomato", "Price": 8.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 41, "Name": "Steak Frites", "Description": "Grilled steak served with French fries", "Price": 19.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 42, "Name": "Coq au Vin", "Description": "Chicken braised in red wine with mushrooms and onions", "Price": 17.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 43, "Name": "Ratatouille", "Description": "Stewed vegetable dish with tomatoes zucchini and eggplant", "Price": 12.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 44, "Name": "Beef Bourguignon", "Description": "Beef stew braised in red wine with carrots and potatoes", "Price": None, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 45, "Name": "Chicken Curry", "Description": "Spicy chicken curry served with rice", "Price": None, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 46, "Name": "Butter Chicken", "Description": "Creamy tomato based chicken curry served with naan", "Price": 15.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 47, "Name": "Lamb Rogan Josh", "Description": "Spiced lamb curry with yogurt and tomatoes", "Price": 16.99, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 48, "Name": "Vegetable Biryani", "Description": "Spiced rice with mixed vegetables", "Price": None, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 49, "Name": "Pad Thai", "Description": "Stir fried rice noodles with shrimp peanuts and lime", "Price": None, "AvailabilityStatus": "In Stock", "ImageURL": ""},
    {"DishID": 50, "Name": "Green Curry", "Description": "Spicy green curry with chicken and vegetables", "Price": None, "AvailabilityStatus": "In Stock", "ImageURL": ""}
]

# Convert the data to a DataFrame
dishes_df = pd.DataFrame(dishes)

# Specify the directory where you want to save the file
output_directory = 'C:/Users/ASUS/Desktop/project-root 9-9 3/recommendation_service'
output_file = os.path.join(output_directory, 'dishes.csv')

# Check and create the directory if it does not exist
os.makedirs(output_directory, exist_ok=True)

# Save the DataFrame to a CSV file
dishes_df.to_csv(output_file, index=False)

print(f"Dishes data has been successfully saved to {output_file}")
print("Current Working Directory:", os.getcwd())
