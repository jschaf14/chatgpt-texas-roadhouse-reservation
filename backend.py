from flask import Flask, jsonify, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import requests
import json

app = Flask(__name__)
job_ids = {}
CORS(app)  # This will enable CORS for all routes

# Helpers
def submit_wait_time_request(data, min_wait_time):
    url = f"https://www.texasroadhouse.com/texasroadhouse/waitlist/{data['extref']}/submit"
    payload = {
        "Attributes": None,
        "EmailAddress": data['email'],
        "FirstName": data['firstName'],
        "IsSmoking": False,
        "LastName": data['lastName'],
        "nomnom": {
            "specialItems": []
        },
        "PartySize": int(data['partySize']),
        "Platform": "web",
        "PrimaryPhoneAreaCode": data['phoneNumber'][:3],
        "PrimaryPhoneExtension": "",
        "PrimaryPhoneNumber": data['phoneNumber'][3:6] + '-' + data['phoneNumber'][6:],
        "PrimaryPhoneType": 1,
        "WaitMinutes": min_wait_time
    }    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    return response

def check_max_reservation_time(extref, party_size):
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0'})
    response = s.get(f'https://www.texasroadhouse.com/texasroadhouse/waitlist/{extref}/quote')
    wait_time = response.json()[party_size]['MaxQuote']
    return wait_time

def check_min_reservation_time(extref, party_size):
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0'})
    response = s.get(f'https://www.texasroadhouse.com/texasroadhouse/waitlist/{extref}/quote')
    wait_time = response.json()[party_size]['MinQuote']
    return wait_time

def wait_time_scheduler(data, scheduler):
    # TODO: Implement logic to check if max wait time plus current time is equal to or higher than the reservation time
    # If the condition is met, call a function and stop the job
    print('Checking reservation time...')
    # Get current time
    now = datetime.datetime.now()

    # Calculate minutes past midnight
    current_minutes = now.hour * 60 + now.minute

    reservationTimeParts = data['reservationTime'].split(':');
    reservationMinutes = int(reservationTimeParts[0]) * 60 + int(reservationTimeParts[1]);
    print(data)
    if check_max_reservation_time(data['extref'], data['partySize']) + current_minutes >= reservationMinutes:
        min_wait_time = check_min_reservation_time(data['extref'], data['partySize'])
        print(submit_wait_time_request(data, min_wait_time))

        scheduler.remove_job(job_ids[data['extref']])
        # Remove the job ID from the dictionary
        del job_ids[data['extref']]

# Routes
@app.route('/get_locations', methods=['GET'])
def get_locations():
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0'})
    response = s.get('https://www.texasroadhouse.com/restaurants')
    locations = response.json()['restaurants']
    return jsonify(locations)

@app.route('/get_wait_time/<extref>/<party_size>', methods=['GET'])
def get_wait_time(extref, party_size):
    return jsonify(check_max_reservation_time(extref, party_size))

@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    data = request.json

    # Start the job when a reservation is submitted
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(func=wait_time_scheduler, args=[data, scheduler], trigger="interval", minutes=1)
    scheduler.start()

    # Store the job ID in the dictionary using the extref as the key
    job_ids[data['extref']] = job.id

    return jsonify({'message': 'Reservation received!'}), 200

if __name__ == '__main__':
    app.run(debug=True)