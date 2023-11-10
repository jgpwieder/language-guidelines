import requests
import json
import random
import time

# URL for the POST request
url = "http://0.0.0.0:8000/users"


# Function to generate random data for the request body
def generate_random_data():
    names = ["Alice", "Bob", "Charlie", "David", "Eva"]
    nicknames = ["user1", "user2", "user3", "user4", "user5"]
    birth_dates = ["01-01-1990", "02-15-1985", "03-20-1995", "04-10-1980", "05-05-2000"]

    return {
        "name": random.choice(names),
        "nickname": random.choice(nicknames),
        "birth": random.choice(birth_dates),
    }


# Number of inserts
num_inserts = 50000

# Time interval between requests (in seconds)
time_interval = 60 / (num_inserts / 10)

# Perform inserts
for _ in range(num_inserts):
    data = generate_random_data()
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        print(f"Insert successful: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error during insert: {e}")

    # Sleep for the specified time interval
    time.sleep(time_interval)
