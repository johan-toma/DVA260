import datetime
import io
import os
from flask import Flask, Response, jsonify, render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from pymongo import MongoClient
import json
from bson import json_util
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from OpenSSL import SSL 

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client.weather_data
measurements = db.measurements


##Shows everythign stored inside the measurement collection in weather_data db. (this is justa test)
@app.route('/')
def index():
    return render_template('index.html')

#render showtable.html template and display all data in the measurement collection in table form
@app.route('/showtable')
def showtable():
    data=list(measurements.find({}))
    return render_template('showtable.html',data=data)

##this must be used to refomat the timestamp it to a datetime object, helper function to parse timestamp
def parse_time(timestamp_string):
    reformat_time = datetime.datetime.strptime(timestamp_string, "%Y-%m-%dTIME:%H:%M:%S")
    return reformat_time

#Display graph of temperature trends over time
@app.route('/displaygraph')
def displaygraph():
    ##fetch in ascenidng order the temperature data and timestamps from mongodb
    graphdata = measurements.find({}, {'_id': 0,'timestamp': 1, 'temperature': 1 }).sort("timestamp", 1)
    #fo each doc returned by a mongodb query in the result set, add to lists the data for plotting
    timestamps = []
    temperatures = []
    #put timestamps and temperatures frooom mongodb results into the lists
    for data in graphdata:
        timestamp = parse_time(data['timestamp'])
        temperature = data['temperature']
        timestamps.append(timestamp)
        temperatures.append(temperature)
    #temperatures = y and timestamps = x
    #a lot of data should need atleast hour or minute to be shown instead cuz its adding new data every 5seconds, or it will clutter ggraph
    #filter data for better visualization
    filtered_timestamps = timestamps[::100]
    filtered_temperatures = temperatures[::100]
    #create and render the graph
    fig = creategraph(filtered_timestamps, filtered_temperatures)
    #save image to bytesio buffer
    image = io.BytesIO()
    FigureCanvas(fig).print_png(image)
    return Response(image.getvalue(), mimetype='image/png')

#render graph based on timestamps and temperatures
def creategraph(timestamps, temperatures):
    fig = Figure()
    #1 row 1 column index 1
    #add subplot to figure
    axis = fig.add_subplot(1,1,1)
    #plots temperature over timestamps
    axis.plot(timestamps, temperatures, marker='o', linestyle='-')
    
    #handle x axis as dates which it is and also increase reeadabiity by auto formating
    #set date format for x-axis and hourlocator for positions of ticks at hourly intervals (1hr)
    axis.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    axis.xaxis.set_major_formatter(mdates.DateFormatter('%m/%dT%H:%M'))
    fig.autofmt_xdate()
    #set the x-axis and y-axis labels and also set name for the plot
    axis.set_xlabel('Timestamps')
    axis.set_ylabel('Temperatures')
    axis.set_title('Temperature trends over time')
    return fig

#display max temp in the database
@app.route('/maxtemp')
def maxtemp():
    #only interested in the max value and not its occcurences, just the maximum value that can be seen uin databas
    #sort by temperature in descending order and get the first result
    #basically find document with the maximum temperature
    max_temp = measurements.find().sort("temperature", -1).limit(1).next()
    max_temp = max_temp.get('temperature')
    return f"<h1>Max temp in database : {max_temp}Celsius</h1>"

#calc the average temp in database and display it
@app.route('/avgtemp')
def avgtemp():
    ####group all documents together then compute the average value of temperature
    #get all temperatures then putin a list, calculate theaverage value of temperatures through the list
    temperatures = measurements.find({}, {"temperature": 1, "_id": 0})
    list_temp = []
    for temperature in temperatures:
        if 'temperature' in temperature:
            list_temp.append(temperature['temperature'])
    
    sum_temp = sum(list_temp)
    count = len(list_temp)
    #display the average value
    return f"<h1>The average temperatures: {sum_temp/count:.2f} Celsius</h1>"

#count and display the total number of documents inside the database
@app.route('/totalentries')
def countentries():
    #fetch all temperature values from mongodb
    temperatures = measurements.find({}, {"temperature": 1, "_id": 0})
    #put these temps inside the list through the loop
    list_temp = []
    for temperature in temperatures:
        if 'temperature' in temperature:
            list_temp.append(temperature['temperature'])
    #count the elements inside list_temp
    count = len(list_temp)
    return f"<h1>The total amount of entries inside the database: {count} entries</h1>"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000, ssl_context=('/home/johan/Documents/GitHub/DVA260/FlaskApp/cert.pem', '/home/johan/Documents/GitHub/DVA260/FlaskApp/key.pem'))
