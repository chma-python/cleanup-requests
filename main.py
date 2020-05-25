from flask import Flask, request, jsonify, make_response
from twilio.rest import Client
import os
import json
import requests

app = Flask(__name__)


account_sid = os.environ['ACCOUNT_SID']
twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']
airtable_auth_token = os.environ['AIRTABLE_AUTH_TOKEN']
to_number = os.environ['ANDY_NUMBER']
chma_number = os.environ['CHMA_NUMBER']

client = Client(account_sid, twilio_auth_token)

@app.route('/funky/', methods=['GET'])
def pollAirtable():
    url = 'https://api.airtable.com/v0/app4QOHvFilnp0nMi/pieces'
    headers = {"Authorization": "Bearer {}".format(airtable_auth_token)}
    params = {
            'maxRecords': 10,
            'view':'Grid view',
            'sortField':'edited',
            'sortDirection': 'desc'
        }

    r = requests.get(url, headers=headers, params=params)

    if r.status_code == 200:
        output_ = [(r['fields']['Name'], r['fields']['Done']) for r in r.json()['records'] if 'Done' in r['fields']]
        
        if ('markers', True) in output_:
            body = """
            \U0001F31F markers is True!
            """           
            
        else:
            body = "markers is not True"
            print(output_)

        message = client.messages.create(
                                  from_=chma_number,
                                  body=body,
                                  to=to_number)

        # print(message.sid)
        return message.sid, 200
            
    else:
        # print('error')
        return 'error', r.status_code

if __name__ == "__main__":
    app.run(port=3000)