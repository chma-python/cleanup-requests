from flask import Flask, request, jsonify, make_response
from twilio.rest import Client
import os
import json
import requests

app = Flask(__name__)


account_sid = os.environ['ACCOUNT_SID']
twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']
airtable_auth_token = os.environ['AIRTABLE_AUTH_TOKEN']

andy_number = '+13144971398'
will_number = '+19087938789'

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
            \U0001F31F
            """ + str("HELLO WILL")            
            
        else:
            body = "HELLO WILL"
            print(output_)

        message = client.messages.create(
                                  from_='+13474180185',
                                  body=body,
                                  to=will_number)

        # print(message.sid)
        return message.sid, 200
            
    else:
        # print('error')
        return 'error', r.status_code

if __name__ == "__main__":
    app.run(port=3000)