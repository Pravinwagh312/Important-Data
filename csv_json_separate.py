import os
import pandas as pd

# Specify the path to the folder containing the CSV files
folder_path = "E:\\Kpit data transform"

# Specify the columns to exclude
exclude_cols = ["title", "another_title"]

# Loop through all the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        # Read the CSV file into a Pandas DataFrame
        csv_df = pd.read_csv(os.path.join(folder_path, filename))

        # Remove the columns to exclude
        csv_df = csv_df.drop(columns=[col for col in csv_df.columns if any(exclude in col.lower() for exclude in exclude_cols)])

        # Write the DataFrame to a JSON file with the same name as the CSV file
        json_filename = os.path.splitext(filename)[0] + ".json"
        csv_df.to_json(os.path.join(folder_path, json_filename), orient="records", indent=4)

        print(f"Converted {filename} to {json_filename}")
