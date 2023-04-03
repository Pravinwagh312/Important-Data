import os
import xmltodict
import pandas as pd
import json

# Set the path to the directory containing the XML files
xml_dir_path = 'F:\XML'

# Define a list of parameter names to exclude from the resulting JSON
exclude_params = ['timestamp']

# Loop through all files in the directory
for filename in os.listdir(xml_dir_path):
    if filename.endswith('.xml'):
        # Construct the full path to the XML file
        xml_file_path = os.path.join(xml_dir_path, filename)
        
        # Parse the XML data and convert it to a pandas DataFrame
        with open(xml_file_path, 'r') as xml_file:
            xml_data = xml_file.read()
        xml_dict = xmltodict.parse(xml_data, attr_prefix='')
        df = pd.json_normalize(xml_dict['testsuites']['testsuite']['testcase'])
        
        # Drop unwanted columns from the DataFrame
        df.drop(exclude_params, axis=1, inplace=True, errors='ignore')
        
        # Construct the full path to the corresponding JSON file
        json_file_path = os.path.splitext(xml_file_path)[0] + '.json'
        
        # Convert the DataFrame to a JSON string and write it to the JSON file
        json_data = df.to_json(orient='records', indent=4)
        with open(json_file_path, 'w') as json_file:
            json_file.write(json_data)
