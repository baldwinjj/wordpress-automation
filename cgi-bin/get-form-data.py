#!/usr/bin/python3

# To Use:
# * Run a local server:
#   python3 -m http.server --bind localhost --cgi 8000
# * Go to the webpage where the form is you'd like to retrieve data from
# * Change the form action to send the data to http://localhost:8000/cgi-bin/get-form-data.py
# * Submit the form (you will be redirected to a view of the json)
# * The form data will be loaded in /data/formData.json

import cgi, cgitb
import os
import json
import csv

def cgiFieldStorageToDict(fieldStorage):
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params

# Get Fields
dataDictionary = cgiFieldStorageToDict(cgi.FieldStorage())
dirname = os.path.dirname(__file__)
jsonString = json.dumps(dataDictionary, indent=4)

# Write to CSV File
filename = os.path.join(dirname, '../data/formData.csv')
with open(filename, 'w') as outputFile:
    writer = csv.writer(outputFile)
    for key, value in dataDictionary.items():
        writer.writerow([key, value])

# Output to the browser
print("Content-Type: application/json; charset=utf-8")
print()
print(jsonString)