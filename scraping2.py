from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Safari()

url = 'https://fso.ueat.utoronto.ca/FSO/ServiceMenuReport/Today'
driver.get(url)

driver.implicitly_wait(10)

html = driver.page_source
driver.quit()

soup = BeautifulSoup(html, 'html.parser')

table = soup.find('div', {'id': 'reportBody'}).find('table')

if table is None:
    raise ValueError("No table found on the webpage")

headers = ['Menu Item', 'Serving Size', 'Calories', 'Fat (g)', 'Saturated Fat (g)', 'Cholesterol (mg)', 'Sodium (mg)', 'Carbohydrate (g)', 'Total Fiber (g)', 'Sugars (g)', 'Protein (g)', 'Vitamin C (mg)', 'Calcium (mg)', 'Iron (mg)']

rows = []
for row in table.find_all('tr'):
    cols = row.find_all('td')
    if cols:
        cols = [ele.text.strip() for ele in cols]
        rows.append(cols)

for row in rows:
    print(len(row), row)

if not rows:
    print("No data rows found in the table.")
else:
    print(f"Found {len(rows)} rows.")

print("Headers:", headers)
print("Number of headers:", len(headers))

if rows:
    print("Length of the first row:", len(rows[0]))

if rows and len(headers) == len(rows[0]):
    df = pd.DataFrame(rows, columns=headers)
else:
    df = pd.DataFrame(rows)

df.to_csv('menu_data.csv', index=False)

print(df)

