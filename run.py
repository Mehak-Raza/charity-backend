import json
import time
from eve import Eve
from flask import request
from flask_cors import CORS, cross_origin
from bson import json_util

app = Eve()
CORS(app)
mongo = app.data.driver


@app.route('/pay', methods=['POST'])
def pay_charity():
    params = json.loads(request.data)
    sender = params.get('sender', None)
    receiver = params.get('charity_name', None)
    amount = params.get('amount', None)

    #Charity
    charity = mongo.db.charity
    receiver_obj = charity.find_one({"name": receiver})
    if not receiver_obj:
        return 'Charity not found'

    person = mongo.db.person
    sender_obj = person.find_one({"name": sender})
    if not sender_obj:
        return 'User not found'

    donation = {
        'receiver': receiver,
        'sender': sender,
        'amount': amount,
        'epoch': int(time.time())
    }

    receiver_obj['contributor'].append(donation)
    if 'contributions' not in sender_obj:
        sender_obj['contributions'] = []
    sender_obj['contributions'].append(donation)
    receiver_obj['fund_raised'] += int(amount)
    charity.update({'name': receiver}, receiver_obj)
    person.update({'name': sender}, sender_obj)

    return json.dumps(receiver_obj, default=json_util.default)



if __name__ == '__main__':
    app.run()

