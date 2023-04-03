import os
import pandas as pd

# Set path to directory containing HTML files
html_dir = '/path/to/html/files'

# Get list of HTML files in directory
html_files = [f for f in os.listdir(html_dir) if f.endswith('.html')]

# Loop through each HTML file
for html_file in html_files:
    # Extract name for JSON output file
    json_file = os.path.splitext(html_file)[0] + '.json'
    
    # Read HTML file and extract all tables
    html_path = os.path.join(html_dir, html_file)
    tables = pd.read_html(html_path)

    # Create empty list to store table data
    data = []

    # Loop through each table and convert to dictionary
    for table in tables:
        table_dict = table.to_dict(orient='split')
        data.append(table_dict)

    # Save table data as JSON file with original HTML file name
    json_path = os.path.join(html_dir, json_file)
    with open(json_path, 'w') as f:
        f.write(pd.io.json.dumps(data, indent=4))
