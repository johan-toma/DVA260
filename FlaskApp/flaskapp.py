from flask import Flask, jsonify, render_template
from pymongo import MongoClient
import json
from bson import json_util

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client['weather_data']
weather_data = db['weather_data']
##main page used to redirect to the different functionalities
@app.route('/')
def index():
    documents = list(weather_data.find({}))
    jsonify_documents = json.loads(json_util.dumps(documents))
    return jsonify(jsonify_documents)


@app.route('/showtable')
def showtable():
    data=list(collection.find({}))
    return render_template('showtable.html',data=data)


@app.route('/displaygraph')
def displaygraph():
    return ""



@app.route('/maxtemp')
def maxtemp():
    pipeline=[
        {"$group":{
           "_id":"$temperature",
           "max_temperature":{"$max":"$temperature"}
    }}
    ]
    data=list(collection.aggregate(pipeline))
    return render_template('maxtemp.html',data=data)


@app.route('/avgtemp')
def avgtemp():
    pipeline= [{"$group":{
        "_id":None,
        "average":{"$avg":"$temperature"}
    }
    }
]
 average=list(collection.aggregate(pipeline))[0]["average"]
return render_template('avgtemp.html', average=average)



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)

