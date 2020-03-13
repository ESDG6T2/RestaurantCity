from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pika, os, json, requests
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/restaurant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)
# FIXME: something wrong with send_order
def send_order(order):
    hostname = 'localhost'
    port = 5555
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    channel = connection.channel()
    
    exchange_name = 'order_direct'
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
    
    channelqueue = channel.queue_declare(queue='order_direct')

    message = json.dumps(order,default=str)

     
    # TODO: if payment fails, send back to Cart

    # if payment succeed, send to Order
    channel.queue_declare(queue='order', durable=True)
    channel.queue_bind(exchange=exchange_name, queue='order', routing_key='order_create')
    channel.basic_publish(exchange=exchange_name, routing_key='order_create', body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    
    # trial run send monitoring
    # no need to create queue
    exchange_name = 'order_fanout'
    channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
    channel.basic_publish(exchange=exchange_name,routing_key='order_update',body=message)
    print('Payment succeeded, order is sent')

@app.route('/payment',methods=['POST'])
def pay_order():
    print('call pay_order')
    order = None
    order = request.get_json()
    order['order_status'] = 'paid'
    paid = True
    print(order)
    print()
    if paid:
        # send_order(jsonify(order))
        return jsonify(order), 200
    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5555,debug=True)