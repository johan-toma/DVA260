from flask import Flask
from pymongo import MongoClient
import os
import time
from datetime import datetime
import json

mongo = os.getenv("MONGO_URI")
client = MongoClient('localhost', 27017)

db = client.weather_data
measurements = db.measurements

#ensure unique values are entered meaning no same entry/duplicate entries
measurements.create_index([("timestamp", 1)], unique=True)


def store_file(data_filepath):
    lines = ""
    if not os.path.exists(data_filepath):
        print(f"Error no file found at {data_filepath}")
        return
    
    with open(data_filepath, 'r') as file:
        lines = file.readlines()
    
    #clear file, after taking the contents
    with open(data_filepath, 'w') as file:
        pass

    #attempt to put each line as adocument inside mongodb
    for line in lines:
        try: 
            doc = json.loads(line.strip())
            measurements.insert_one(doc)
            print(f"Inserted: {doc}")
        except Exception as error:
            print(f"Error insering document {error}")

if __name__ == '__main__':
    data_filepath = "/svolume/data.txt"
    while True:
        store_file(data_filepath)
        time.sleep(5)
    



