import os
import pandas as pd

# Specify the path to the folder containing the XML files
folder_path = "E:\\Kpit data transform"

# Specify the columns to exclude
exclude_cols = ["title", "genre", "price"]

# Loop through all the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".xml"):
        # Read the XML file into a Pandas DataFrame
        xml_df = pd.read_xml(os.path.join(folder_path, filename))

        # Remove the columns to exclude
        xml_df = xml_df.drop(columns=[col for col in xml_df.columns if any(exclude in col.lower() for exclude in exclude_cols)])

        # Write the DataFrame to a JSON file with the same name as the XML file
        json_filename = os.path.splitext(filename)[0] + ".json"
        xml_df.to_json(os.path.join(folder_path, json_filename), orient="records", indent=4)

        print(f"Converted {filename} to {json_filename}")
