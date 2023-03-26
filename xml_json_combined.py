import os
import pandas as pd

# Specify the path to the folder containing the XML files
folder_path = "E:\\Kpit data transform"

# Specify the columns to exclude
exclude_cols = ["title", "another_title"]

# Create an empty dictionary to store the dataframes for each file
data_dict = {}

# Loop through all the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".xml"):
        # Read the XML file into a Pandas DataFrame
        xml_df = pd.read_xml(os.path.join(folder_path, filename))

        # Remove the columns to exclude
        xml_df = xml_df.drop(columns=[col for col in xml_df.columns if any(exclude in col.lower() for exclude in exclude_cols)])

        # Add the DataFrame to the dictionary
        data_dict[filename] = xml_df

# Concatenate all the DataFrames into a single DataFrame
combined_df = pd.concat(data_dict.values(), ignore_index=True)

# Write the combined DataFrame to a JSON file
combined_df.to_json(os.path.join(folder_path, "combined.json"), orient="records", indent=4)

print(f"Converted {len(data_dict)} files to combined.json")
