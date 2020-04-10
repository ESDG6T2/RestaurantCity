from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

import pika, json, requests, uuid, pytz

from datetime import datetime
# import paypalrestsdk
tz = pytz.timezone('Asia/Singapore')
app = Flask(__name__)
CORS(app)
def generate_order_id():
    return uuid.uuid4().hex

# Note: port must be 5672 for pika

@app.route('/successpayment',methods=['POST'])
def success_order():
    if request.is_json:
        order = request.get_json()
        for i in range(len(order['orderItems'])):
            order['orderItems'][i]['menuId'] = order['orderItems'][i].pop('sku')
        order['orderStatus']='paid'
        order['orderId'] = generate_order_id()
        order['orderDatetime'] = datetime.now(tz).strftime(format='%Y-%m-%d %H:%M:%S')
    else:
        order = request.get_data()
        print("Received an invalid order:")
        print(order)
        replymessage = json.dumps({"message": "Order should be in JSON", "data": order}, default=str)
        return replymessage, 400 # Bad Request
    print("Payment is successful")
    try:
        r = requests.post(url='http://host.docker.internal:8010/add-order/{}'.format(order['orderId']), json=order)
        if r.status_code == 201:
            return jsonify({'message': 'Successfully submitted the order'}), 200
        else:
            return jsonify({'message':'Order submission failed '}), 500
    except:
        return jsonify({'message':'Order submission failed '}), 500
    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5555,debug=True)


