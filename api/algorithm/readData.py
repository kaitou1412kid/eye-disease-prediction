import json
import os

def openFile():
    with open('data.json','r') as f:
        json_data = json.load(f)
    return json_data

def readData(disease):
    json_data = openFile()
    return json_data[disease]
    
