import os
import pandas as pd
from bs4 import BeautifulSoup

# Define the path to the folder containing the HTML files
folder_path = "E:\Kpit data transform"

# Define the list of columns to exclude from the JSON output
exclude_cols = ["parameter1", "parameter2"]

# Loop through all the files in the folder with the ".html" extension
for filename in os.listdir(folder_path):
    if filename.endswith(".html"):
        # Read the HTML file into a BeautifulSoup object
        with open(os.path.join(folder_path, filename), encoding="utf8") as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')

        # Extract the data from the HTML table and convert it to a DataFrame
        table = soup.find('table')
        html_df = pd.read_html(str(table))[0]

        # Drop the specified columns from the DataFrame
        html_df = html_df.drop(exclude_cols, axis=1)

        # Write the DataFrame to a JSON file with the same name as the HTML file
        json_filename = os.path.splitext(filename)[0] + ".json"
        html_df.to_json(os.path.join(folder_path, json_filename), orient="records", indent=4)

        print(f"Converted {filename} to {json_filename}")