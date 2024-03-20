# Import necessary libraries
import csv
import openai
import os
from datetime import date

# Load OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
# Initialize OpenAI client with API key
openai.api_key = api_key

# Open CSV file containing ingredients
with open(os.getenv('CSV_FILE_PATH'), 'r') as file:
    # Create CSV reader to read the file
    reader = csv.reader(file)
    # Read all data from the file into a list
    data = list(reader)

# Get number of recipes to generate from environment variables
num_recipes = int(os.getenv('NUM_RECIPES'))

# Get filters from environment variables
total_cost = float(os.getenv('TOTAL_COST'))  # Desired total cost
is_vegan = os.getenv('IS_VEGAN').lower() == 'true'  # Whether recipes should be vegan
total_servings = int(os.getenv('TOTAL_SERVINGS'))  # Desired number of servings

# Create message for AI
message = f"Create {num_recipes} recipes using these ingredients: {data}. Each recipe should have a total cost of around {total_cost}, be vegan: {is_vegan}, and serve {total_servings} people. Please provide a name, short description, and a list of ingredients with their costs for each recipe."

# Request a completion from AI
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": message
        }
    ]
)

# Extract recipes from response
recipes = response['choices'][0]['message']['content']
file_path = f'data/requestedRecipes/metro/recipes_{date.today()}.csv'
# Save recipes to a CSV file
with open(file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Description", "Ingredients", "Cost per Ingredient", "Total Cost"])
    for recipe in recipes:
        writer.writerow([recipe['name'], recipe['description'], recipe['ingredients'], recipe['cost_per_ingredient'], recipe['total_cost']])
