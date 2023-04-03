import os
import xmltodict
import json

# Set the path to the directory containing the XML files
xml_dir_path = 'F:\XML'

# Loop through all files in the directory
for filename in os.listdir(xml_dir_path):
    if filename.endswith('.xml'):
        # Construct the full path to the XML file
        xml_file_path = os.path.join(xml_dir_path, filename)
        
        # Parse the XML data and convert it to a Python dictionary
        with open(xml_file_path, 'r') as xml_file:
            xml_data = xml_file.read()
        xml_dict = xmltodict.parse(xml_data, attr_prefix='')
        
        # Construct the full path to the corresponding JSON file
        json_file_path = os.path.splitext(xml_file_path)[0] + '.json'
        
        # Convert the Python dictionary to a JSON string and write it to the JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(xml_dict, json_file, indent=4)
