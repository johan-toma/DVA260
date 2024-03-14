import datetime
import io
from flask import Flask, Response, jsonify, render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from pymongo import MongoClient
import json
from bson import json_util
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client.weather_data
measurements = db.measurements


##Shows everythign stored inside the measurement collection in weather_data db. (this is justa test)
@app.route('/')
def index():
    documents = list(measurements.find({}))
    jsonify_documents = json.loads(json_util.dumps(documents))
    return jsonify(jsonify_documents)


@app.route('/showtable')
def showtable():
    data=list(measurements.find({}))
    return render_template('showtable.html',data=data)

##this must be used to refomat the timestamp it to a datetime object
def parse_time(timestamp_string):
    reformat_time = datetime.datetime.strptime(timestamp_string, "%Y-%m-%dTIME:%H:%M:%S")
    return reformat_time

@app.route('/displaygraph')
def displaygraph():
    ##fetch in ascenidng order the temperature data and timestamps from mongodb
    graphdata = measurements.find({}, {'_id': 0,'timestamp': 1, 'temperature': 1 }).sort("timestamp", 1)
    #fo each doc returned by a mongodb query in the result set, add to lists the data for plotting
    timestamps = []
    temperatures = []
    for data in graphdata:
        timestamp = parse_time(data['timestamp'])
        temperature = data['temperature']
        timestamps.append(timestamp)
        temperatures.append(temperature)
    #temperatures = y and timestamps = x
    #plt.plot(timestamps, temperatures)
    #plt.xlabel("Time")
    #plt.ylabel("Temperatures (Celsius)")
    #plt.title("Temperature Trends")
    #choose every x-th to solve overcrowding
    filtered_timestamps = timestamps[::25]
    filtered_temperatures = temperatures[::25]
    fig = creategraph(filtered_timestamps, filtered_temperatures)
    #save image to bytesio buffer
    image = io.BytesIO()
    FigureCanvas(fig).print_png(image)
    return Response(image.getvalue(), mimetype='image/png')


def creategraph(timestamps, temperatures):
    fig = Figure()
    #1 row 1 column index 1
    axis = fig.add_subplot(1,1,1)
    axis.plot(timestamps, temperatures, marker='o', linestyle='-')
    #axis.scatter(timestamps, temperatures)
    #handle x axis as dates which it is and also increase reeadabiity by auto formating
    #axis.xaxis_date()
    #a lot of data should need atleast hour or minute to be shown instead cuz its adding new data every 5seconds, or it will clutter ggraph
    axis.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    axis.xaxis.set_major_formatter(mdates.DateFormatter('%m/%dT%H:%M'))
    fig.autofmt_xdate()

    
    axis.set_xlabel('Timestamps')
    axis.set_ylabel('Temperatures')
    axis.set_title('Temperature trends over time')
    return fig

@app.route('/maxtemp')
def maxtemp():
    #only interested in the max value and not its occcurences, just the maximum value that can be seen uin databas
    #sort by temperature in descending order and get the first result
    max_temp = measurements.find().sort("temperature", -1).limit(1).next()
    max_temp = maxtemp.get('temperature')
    return f"<h1>Max temp in database : {max_temp}Celsius</h1>"


@app.route('/avgtemp')
def avgtemp():
    ####group all documents together then compute the average value of temperature
    #avgtemp = measurements.aggregate([{"$project": {"tempCount": {"$sum": "$temperature"}}}, {"$group": {"_id": None, "averageTemp": {"$avg": "$tempCount"}}}])
    #get all temperatures then putin a list, calculate theaverage value of temperatures through the list
    temperatures = measurements.find({}, {"temperature": 1, "_id": 0})
    list_temp = []
    for temperature in temperatures:
        if 'temperature' in temperature:
            list_temp.append(temperature['temperature'])
    
    sum_temp = sum(list_temp)
    count = len(list_temp)
    return f"<h1>The average temperatures: {sum_temp/count:.2f} Celsius</h1>"

@app.route('/totalentries')
def countentries():
    temperatures = measurements.find({}, {"temperature": 1, "_id": 0})
    list_temp = []
    for temperature in temperatures:
        if 'temperature' in temperature:
            list_temp.append(temperature['temperature'])
    
    count = len(list_temp)
    return f"<h1>The total amount of entries inside the database: {count} entries</h1>"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
