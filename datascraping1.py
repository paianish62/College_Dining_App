import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# URL of the website to scrape
url = "https://vicu.utoronto.ca/hospitality-services/student-meal-plans-and-dining-hall-menus/burwash-dining-hall/"

# Send a GET request to fetch the raw HTML content
response = requests.get(url)
response.raise_for_status()

# Parse the content of the request with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize a list to store the food items
food_items = []

# Define headers to exclude
headers_to_exclude = ["BYOGLUTENFREE", "SOUPS", "ENTRÉE", "VEGETARIANENTRÉE", "SIDES"]

# Locate the relevant section of the page
menu_section = soup.find_all('table')

for table in menu_section:
    rows = table.find_all('tr')
    for row in rows:
        columns = row.find_all('td')
        for col in columns:
            text = col.get_text(strip=True)
            if text and text not in headers_to_exclude:
                # Split combined items into separate items based on bullet points
                items = re.split(r'•\s*', text)
                food_items.extend(items)

# Define a function to check for dietary labels
def check_label(item, label):
    return 'Yes' if label in item else 'No'

# Define a function to remove dietary labels
def remove_labels(item):
    return re.sub(r'\s*\(.*?\)', '', item).strip()

# Create a DataFrame to store the menu items and their labels
data = {
    'Food': [],
    'Halal': [],
    'Gluten Free': [],
    'Dairy Free': [],
    'Vegetarian': [],
    'Vegan': []
}

# Populate the DataFrame
for item in food_items:
    item = item.strip()
    if item:  # Ensure the item is not empty
        data['Food'].append(remove_labels(item))
        data['Halal'].append(check_label(item, '(H)'))
        data['Gluten Free'].append(check_label(item, '(GF)'))
        data['Dairy Free'].append(check_label(item, '(DF)'))
        data['Vegetarian'].append(check_label(item, '(VEG)'))
        data['Vegan'].append(check_label(item, '(VGN)'))

df = pd.DataFrame(data)

# Display the DataFrame
print(df)
