import requests
import json
import logging
import time
import os
from dotenv import load_dotenv
from quixstreams import Application

# --- How to get data from the API ---

def get_stop_point_info(stop_point_name,mode="tube"):
    if mode not in ["tube", "bus"]:
        raise ValueError("Invalid mode. Mode must be 'tube' or 'bus'.")
    
    response = requests.get(
        "https://api.tfl.gov.uk/StopPoint/Search/" + stop_point_name,
        params = {
            'app_key': app_key
        }
    )
    response_data = response.json()


    results = []


    matches = response_data['matches'] # 'matches' is part of the response structure

    for match in matches:
        if mode in match['modes']:
            results.append({
                'name': match['name'],
                'id': match['id'],
            })
    return results


def get_tube_arrivals(line_id, stop_point_id, direction, app_key, retries=3, backoff=5):
    url = f"https://api.tfl.gov.uk/Line/{line_id}/Arrivals/{stop_point_id}"
    params = {
            'direction': direction,
            'app_key': app_key,
        }
    for attempt in range(retries):
        response = requests.get(url, params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        logging.debug(f"API response: {data}")
        if data:  # If response is not empty, return it
            return data
        
        logging.warning(f"Attempt {attempt+1} returned empty response.")
        time.sleep(backoff * (attempt + 1))  # Exponential backoff

        return [{'vehicleId': 'N/A', 'stationName': 'N/A'}]  # Return default if all retries fail


# --- Get data from the API ---

load_dotenv() #loads the API key your .env file
# create a .env file containing your API key with the below variable
app_key = os.getenv('TFL_API_KEY')

stop="stockwell"
line_id = "victoria"
stop_point_id = [id['id'] for id in get_stop_point_info(stop)] # get the id out of the result
direction = "outbound"

sleep_time = 35



def main(): 
    app = Application(
        broker_address="localhost:19092",
        loglevel="DEBUG",
    )

    with app.get_producer() as producer:
        while True:
            tube = get_tube_arrivals(line_id, stop_point_id[0], direction, app_key)
            # vehicleId, stationName, platformName, timestamp, timeToStation, currentLocation, towards
            if not tube:
                tube = ['N/A']
            vehicleId = tube[0]['vehicleId'] if tube else 'N/A'
            logging.debug(f"Got vehicle: {vehicleId}")
            producer.produce(
                topic="tfl-tubes",
                key=tube[0]['stationName'] if tube else 'N/A',
                value=json.dumps(tube),
                headers= {"app.name": "python-quix"}
            )
            logging.info(f"Produced. Sleeping for {sleep_time}s...")
            time.sleep(sleep_time)

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()