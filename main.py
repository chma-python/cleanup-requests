from twilio.rest import Client
import os
import json
import requests

def cleanupRequests():
    headers = {"Authorization": "Bearer {}".format(os.environ['AIRTABLE_AUTH_TOKEN'])}
    params =  params = {
            'maxRecords': 10,
            'view': 'All Requests + Data',
            'sortField':'Last Modified',
            'sortDirection': 'asc'
        }

    r = requests.get(os.environ['PROD_URL'], headers=headers, params=params)

    completed = [record for record in r.json()['records'] if record['fields']['Status'] == 'Request Complete']

    client = Client(os.environ['ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])

    for record in completed:
        
        data = {
            'fields':
              {'Message': "",
               'First Name': ""
              }
            }

        r = requests.patch(
            os.environ['PROD_URL'] + record['id'] , headers=headers, json=data
        )

        # deletion code should look something like this
        call_sid = record['fields']['Twilio Call Sid']
        recordings = client.recordings.list(call_sid=call_sid)
        for record in recordings:
            client.recordings(record['sid']).delete()

if __name__ == "__main__":
    cleanupRequests()