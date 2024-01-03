import json
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime


# Global variables
cost = 0
m_c = ""
d = ""
current_time = datetime.now()
current_time_str = current_time.isoformat()
user_selections = {"user": "", "cuisine": "", "dish": "", "cost": "","time": "" }

def get_user_input(options, category):
    print("-" * 50)
    print()
    for i, dish in enumerate(options, start=1):
        print(f"{i}. {dish['name']} = {dish['price']}rs")
    selection = int(input(f"Enter the {category} number: "))
    return options[selection - 1]['name'], options[selection - 1]['price']

def get_cuisine_options(cuisine_name, dishes):
    global cost, d
    print("-" * 50)
    print()
    print(f"{cuisine_name} cuisine:")
    d, dish_cost = get_user_input(dishes, "dish")
    cost += dish_cost

def multi_cuisine():
    global m_c
    cuisines = [
        {"name": "North Indian", "dishes": [{"name": "Chole Bhature", "price": 100}, {"name": "Rajma chawal", "price": 50}, {"name": "Paratha", "price": 100}, {"name": "Aloodam Puri", "price": 50}, {"name": "Veg Biryani", "price": 150}]},
        {"name": "South Indian", "dishes": [{"name": "Uttapam", "price": 100}, {"name": "Idli", "price": 50}, {"name": "Vada", "price": 100}, {"name": "Coconut Rice", "price": 50}, {"name": "Dosa", "price": 150}]},
        {"name": "Italian", "dishes": [{"name": "Lasagne", "price": 100}, {"name": "Risotto", "price": 50}, {"name": "Pasta", "price": 100}, {"name": "Gelato (Ice cream)", "price": 50}, {"name": "Pizza", "price": 150}]},
        {"name": "Chinese", "dishes": [{"name": "Chow Mein", "price": 100}, {"name": "Spring Rolls", "price": 50}, {"name": "Dim Sum", "price": 100}, {"name": "Fried Rice", "price": 50}, {"name": "Chilli Manchurian", "price": 150}]},
        {"name": "Mexican", "dishes": [{"name": "Mole", "price": 100}, {"name": "Taco", "price": 50}, {"name": "Gorditas", "price": 100}, {"name": "Arroz con leche", "price": 50}, {"name": "Huevos a la Mexicana", "price": 150}]}
    ]

    c = int(input("1. North Indian (press 1) \n2. South Indian (press 2)\n3. Italian (press 3) \n4. Chinese (press 4) \n5. Mexican (press 5)\n Enter the cuisine number:"))
    m_c = cuisines[c - 1]["name"]
    get_cuisine_options(m_c, cuisines[c - 1]["dishes"])

def print_receipt():
    print("-" * 50)
    print("Cost == {0}\nINCLUDE 18% 'GST'\nTotal payable amount = {1}".format(cost, int((cost / 100) * 18 + cost)))

def save_to_json():
    user_selections.update({"user": user, "cuisine": m_c, "dish": d, "cost": cost, "time": current_time_str})
    try:
        with open("user_selections1.json", "r") as json_file:
            existing_data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []
    existing_data.append(user_selections)
    with open("user_selections1.json", "w") as json_file:
        json.dump(existing_data, json_file, indent=2)

def option():
    n = int(input("Enter number 1 or 2 to continue: "))
    if n == 1:
        print_receipt()
    elif n == 2:
        graph()
    else:
        option()

def graph():
    # Load data from the JSON file
    with open("user_selections1.json", "r") as json_file:
        data = json.load(json_file)

    # Extract dishes from the data
    dishes = [entry["dish"] for entry in data]

    # Count the occurrences of each dish
    dish_counts = Counter(dishes)

    # Get the 5 most ordered dishes
    top_dishes = dish_counts.most_common(5)

    # Extract dish names and their corresponding counts
    dish_names, dish_order_counts = zip(*top_dishes)

    # Plot the bar graph
    plt.bar(dish_names, dish_order_counts, color='blue')
    plt.xlabel('Dish')
    plt.ylabel('Number of Orders')
    plt.title('Top 5 Most Ordered Dishes')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.tight_layout()

    # Show the plot
    plt.show()
    

print("-" * 50)
print("\nWelcome to the Billing and Analytical Application\n")
print("-" * 50)
user = input("Please enter your name: ")
print("-" * 50)
print("\nWhich cuisine would you like to eat:")
multi_cuisine()
save_to_json()

while input("Do you want to continue your order y/n: ") == "y":
    multi_cuisine()
    save_to_json()
    
print("-" * 50)
print("If you want know your billing:(press 1)\nOr you want to see 5 most order dish in your menu:(press 2)")
option()
