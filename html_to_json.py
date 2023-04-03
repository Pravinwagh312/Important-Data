import pandas as pd

# Read HTML file and extract all tables
tables = pd.read_html('report3.html')

# Create empty list to store table data
data = []

# Loop through each table and convert to dictionary
for table in tables:
    table_dict = table.to_dict(orient='split')
    data.append(table_dict)

# Save table data as JSON file
with open('output.json', 'w') as f:
    f.write(pd.io.json.dumps(data,indent=4))
