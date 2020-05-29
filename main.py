from twilio.rest import Client
from flask import Flask
import os
import json
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def cleanupRequests(n=10):
    """
    Finds the last n records in the Requests table where "Status" = "Request Complete" that were last modified at least 30 days ago, erases the "Message" and "First Name" fields and deletes any recordings associated with the call.
    """

    # formula for filtering data from airtable
    formula = 'AND(DATETIME_DIFF(NOW(), {Last Modified}, "days") > 30, Status = "Request Complete")'

    # airtable query
    headers = {"Authorization": "Bearer {}".format(os.environ['AIRTABLE_AUTH_TOKEN'])}
    params =  params = {
            'maxRecords': 10,
            'view': 'All Requests + Data',
            'sortField':'Last Modified',
            'sortDirection': 'asc',
            'filterByFormula': formula

        }


    r = requests.get(os.environ['PROD_URL'], headers=headers, params=params)

    # if status code is good ...
    if r.status_code == 200:

        # instantiate twilio client
        client = Client(os.environ['ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])

        # iterate through records
        for record in r.json()['records']:

            data = {
                'fields':
                  {'Message': "",
                   'First Name': ""
                  }
                }

            # patch the requisite fields
            r = requests.patch(
                os.environ['PROD_URL'] + record['id'] , headers=headers, json=data
            )

            # erase the recordings associated with the call SID
            call_sid = record['fields']['Twilio Call Sid']
            call = client.calls(call_sid).fetch()

            for recording_sid in call.recordings.list():
                client.recordings(recording_sid).delete()

            # confirm deletion
            r = requests.get(os.environ['PROD_URL'] + record['id'], headers=headers)
            call = client.calls(call_sid).fetch()

            if all([r.status_code == 200, 
                   'Message' not in r.json().keys(), 
                   'First Name' not in r.json().keys(),
                   len(call.recordings.list()) == 0]):
                print('succesfully deleted')
                
            else:
                print('error')

if __name__ == "__main__":
    app.run()