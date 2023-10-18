import os
import sys
import xml.etree.ElementTree as ET
import json
from fnmatch import fnmatch
import time
import argparse

# Argument parsing setup
parser = argparse.ArgumentParser(description="Parse XML Reports based on JSON Configuration.")
parser.add_argument("-xml_dir", "--xml_directory", required=True, help="Path to the directory containing XML reports.")
args = parser.parse_args()


jsonFileName = ''
errors = []  # List to capture any errors

def log_error(err_msg):
    """Log error messages and append to the errors list."""
    print(err_msg)
    errors.append(err_msg)

def write_errors_to_json():
    """Write errors to the output JSON if there are any."""
    err_dict = {"errors": errors} if errors else {"message": "No error"}
    outDir = os.path.join(os.getcwd(), "KPI/testStandardization/output")
    err_filename = os.path.join(outDir, 'errors.json')
    with open(err_filename, "w") as f:
        json.dump(err_dict, f, indent=4)
    print("Contents of errors.json:")
    print(json.dumps(err_dict, indent=4))

def writeJSON(jsonDict, jsonFileName):
    try:
        json_object = json.dumps(jsonDict, indent=4)
        outDir = os.path.join(os.getcwd(), "KPI/testStandardization/output")
        if not os.path.isdir(outDir):
            os.mkdir(outDir)
        jsonFileName = os.path.join(outDir, jsonFileName)
        with open(jsonFileName, "w") as outfile:
            outfile.write(json_object)
    except Exception as e:
        log_error(f"Error writing to JSON {jsonFileName}: {str(e)}")

def checks(key, data):
    if key in data:
        return 'pass'
    else:
        return 'next'

def readXML(xmlFile):
    try:
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        return root
    except Exception as e:
        log_error(f"Error parsing XML {xmlFile}: {str(e)}")
        return None

def readJSON(jsonFile):
    jsonAllData = {}
    try:
        data = json.load(jsonFile)
    except Exception as e:
        log_error(f"Error loading JSON {jsonFile.name}: {str(e)}")
        return

    jsonFileName = 'output.json'
    jsonDict = {}

    for k in list(data.keys()):
        jsonDict[k] = {}

        # check XML File
        root = None  # Reset root for each loop iteration
        if checks('xmlFilePath', data[k]) == 'pass':
            for file in os.listdir(args.xml_directory):
                if file.endswith('.xml'):
                    root = readXML(os.path.join(args.xml_directory, file))

        if not root:
            log_error(f"No XML for {k}")
            continue

        lists = []
        # Check if tags exist for all tests
        if checks('tags', data[k]) == 'pass':
            tagName = ''
            alltags = data[k]['tags']
            for i in alltags:
                jsonDict[i] = {}
                for neighbor in root.iter(i):
                    for j in range(0, len(alltags[i])):
                        if alltags[i][j] in jsonDict[k]:
                            tagName = alltags[i][j]
                            lists.append(neighbor.attrib.get(alltags[i][j]))
                        else:
                            jsonDict[k][alltags[i][j]] = neighbor.attrib.get(alltags[i][j])
        else:
            log_error('No Tag data available')
        
        if tagName in jsonDict[k]:
            lists[:0] = [jsonDict[k][tagName]]
            jsonDict[k][tagName] = lists
            jsonAllData.update(jsonDict)
        else:
            jsonAllData.update(jsonDict)
        jsonDict.clear()
    writeJSON(jsonAllData, jsonFileName)

def scanFolder():
    fileName = []
    root = os.path.join(os.getcwd(), 'KPI/testStandardization/configFiles')
    pattern = "*.json"
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                fname = os.path.join(path, name)
                if not os.path.exists(fname):
                    log_error(f"Input JSON file not found: {fname}")
                    continue
                fileName.append(fname)
    return fileName

if __name__ == "__main__":
    start = time.time()
    allInputJsonfiles = scanFolder()
    for config in allInputJsonfiles:
        with open(config) as jsonFile:
            readJSON(jsonFile)

    end = time.time()

    print('time to execute this code is ==> ', end - start, 'sec')

    # Print the content of output.json
    try:
        with open(os.path.join(os.getcwd(), "KPI/testStandardization/output/output.json"), 'r') as f:
            data = json.load(f)
            print(json.dumps(data, indent=4))
    except Exception as e:
        log_error(f"Error reading output.json: {str(e)}")
    
    # Log errors to a separate errors.json if there are any
    write_errors_to_json()
