from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

# for mircoservice connection
import json
import sys
import os
import random

# Communication patterns:
# Use a message-broker with 'direct' exchange to enable interaction
import pika
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/restaurant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class OrderDetail(db.Model):
    __tablename__ = 'orderdetail'

    orderId = db.Column(db.String(45), primary_key=True)
    menuId = db.Column(db.String(45), nullable=False)
    Qty= db.Column(db.Integer, nullable=False)

    def __init__(self, orderId, menuId, Qty):
        self.orderId = orderId
        self.menuId = menuId
        self.Qty = Qty

    def json(self):
        return {"orderId": self.orderId, "menuId": self.menuId, "Qty": self.Qty}

class Orders(db.Model):
    __tablename__ = 'orders'

    orderId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(45), nullable=False)
    billingAddress= db.Column(db.String(45), nullable=False)
    postalCode= db.Column(db.String(45), nullable=False)
    contactNo= db.Column(db.String(45), nullable=False)
    datetime= db.Column(db.DateTime, nullable=False)
    totalAmount=db.Column(db.DECIMAL(6,2), nullable=False)
    orderStatus=db.Column(db.String(45), nullable=False)

    def __init__(self, userId, billingAddress, postalCode,contactNo,totalAmount):
        self.userId = userId
        self.billingAddress = billingAddress
        self.postalCode = postalCode
        self.contactNo = contactNo
        self.datetime=datetime.now()
        self.totalAmount=totalAmount
        self.orderStatus="Paid"

    def json(self):
        return {"orderId": self.orderId, "userId": self.userId, "billingAddress": self.billingAddress, "postalCode": self.postalCode, "contactNo": self.contactNo}


hostname = "localhost" # default hostname
port = 5672 # default port
# connect to the broker and set up a communication channel in the connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
    # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
channel = connection.channel()
# set up the exchange if the exchange doesn't exist
exchangename="order_direct"
channel.exchange_declare(exchange=exchangename, exchange_type='direct')

def receiveOrder():
    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue="restaurant", durable=True) # 'durable' makes the queue survive broker restarts so that the messages in it survive broker restarts too
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='restaurant.order') # bind the queue to the exchange via the key

    # set up a consumer and start to wait for coming messages
    channel.basic_qos(prefetch_count=1) # The "Quality of Service" setting makes the broker distribute only one message to a consumer if the consumer is available (i.e., having finished processing and acknowledged all previous messages that it receives)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True) # 'auto_ack=True' acknowledges the reception of a message to the broker automatically, so that the broker can assume the message is received and processed and remove it from the queue
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("Received an order by " + __file__)
    result = addToDatabase(json.loads(body))
    # print processing result; not really needed
    
    json.dump(result, sys.stdout, default=str) # convert the JSON object to a string and print out on screen
    print() # print a new line feed to the previous json dump
    print() # print another new line as a separator
    return 

def addToDatabase(order):

    orders = Orders(order['userId'], order['billingAddress'], order['postalCode'],order['contactNo'],order['totalAmt'])
    try:
        db.session.add(orders)
        db.session.commit()
    except:
        return ({"message": "Order created successfully."})
    for key, item in order['menuItem'].items():
        orderDetail= OrderDetail(orders.orderId,key,item)
        try:
            db.session.add(orderDetail)
            db.session.commit()
        except:
            return ({"message": "Order created successfully."})
    return ({"message": "Order created successfully."})


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("This is " + os.path.basename(__file__) + ": restaurant for an order...")
    app.run(port=5003, debug=True)
    receiveOrder()