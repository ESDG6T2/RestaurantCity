from flask import Flask, request, jsonify
from flask_cors import CORS

import pika, json, requests, uuid

from datetime import datetime
import paypalrestsdk

app = Flask(__name__)
CORS(app)
def generate_order_id():
    return uuid.uuid4().hex

# Note: port must be 5672 for pika
def send_order(order): # only when paypal payment succeed
    hostname = 'localhost'
    port = 5672
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    channel = connection.channel()
    
    message = json.dumps(order,default=str)

    exchange_name = 'order_direct'
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
    channel.queue_declare(queue='order',durable=True)
    channel.basic_publish(exchange=exchange_name, routing_key='order.receive', body=message,properties=pika.BasicProperties(delivery_mode=2))

    print('Payment succeeded, order is sent')

@app.route('/payment',methods=['POST'])
def pay_order():
    # Assuming payment successful
    order = request.get_json()
    order['orderStatus']='paid'
    order['orderId'] = generate_order_id()
    order['orderDatetime'] = datetime.now().strftime(format='%Y-%m-%d %H:%M:%S')
    print(order)
    send_order(order)
    return jsonify(order), 200

    # TODO: integrating with Paypal
    # Call paypal api here 
    # r = requests.post('http://127.0.01/7000/checkout',json=order)

    # if r.status_code == 200:
    #     send_order(order)
    #     return jsonify(order), 200
    # else:
    #     return jsonify(order), 400
    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5555,debug=True)


