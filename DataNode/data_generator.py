import json
from datetime import datetime
import datetime
import random
import time

def generate_weather_data():
    current_time = datetime.now()
    temperature = random.randint(5, 15)
    humidity = random.randint(15, 25)

    if current_time.hour >= 21 or current_time.hour <= 9:
        temperature = random.randint(-5, 5)
    
    if current_time.month >= 1 or current_time.month <= 6:
        humidity = random.randint(10, 20)
    
    ##return a tuple with the random generated values
    return {
        "timestamp": current_time.strftime("%Y-%m-%dTIME:%H:%M:%S"),
        "sensorname": "Outdoorsensor",
        "temperature": temperature,
        "humidity": humidity
    }


def send_to_volume(data, filepath):
    with open(filepath, "a") as file:
        file.write(json.dumps(data) + "\n")



if __name__ == '__main__':
    data_filepath = "svolume/data.text"
    while True:
        data = generate_weather_data()
        send_to_volume(data, data_filepath)
        time.sleep(5)
