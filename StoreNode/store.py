from flask import Flask
from pymongo import MongoClient, WriteConcern
import os
import time
from datetime import datetime
import json

#connect to mongo
mongo = os.getenv("MONGO_URI")
client = MongoClient("mongodb://mongod:27017/")
#access database and collection
db = client.weather_data
measurements = db.measurements

#ensure unique values are entered meaning no same entry/duplicate entries
measurements.create_index([("timestamp", 1)], unique=True)

#function to store data from a file into mongodb
def store_file(data_filepath):
    lines = ""
    #check if data file exists
    if not os.path.exists(data_filepath):
        print(f"Error no file found at {data_filepath}")
        return
    #open data file and read the contents of it
    with open(data_filepath, 'r') as file:
        lines = file.readlines()
    
    #clear file, after taking the contents
    with open(data_filepath, 'w') as file:
        pass

    #attempt to put each line from file as adocument inside mongodb
    for line in lines:
        try: 
            #parse json data from each line
            doc = json.loads(line.strip())
            
            #insert the document into the measurements collection
            measurements.insert_one(doc)
            print(f"Inserted: {doc}")
        except Exception as error:
            print(f"Error insering document {error}")

if __name__ == '__main__':
    data_filepath = "/svolume/data.txt"
    #continuously store data into mongodb from the data file
    while True:
        store_file(data_filepath)
        time.sleep(5)
    



