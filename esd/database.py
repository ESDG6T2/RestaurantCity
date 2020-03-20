from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/restaurant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

import json
import sys
import os
import random
import datetime
import pika

class User(db.Model):
    __tablename__ = 'user'

    userId = db.Column(db.String(45), primary_key=True)
    password = db.Column(db.String(45), nullable=False)

    def __init__(self, userId, password):
        self.userId = userId
        self.password = password

    def json(self):
        return {"userId": self.userId, "password": self.password}

class Menu(db.Model):
    __tablename__ = 'menu'

    menuId = db.Column(db.String(45), primary_key=True)
    foodName = db.Column(db.String(45), nullable=False)
    price= db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, menuId, foodName, price):
        self.menuId = menuId
        self.foodName = foodName
        self.price = price

    def json(self):
        return {"menuId": self.menuId, "foodName": self.foodName, "price": self.price}


@app.route("/user", methods=['POST'])
def authenicate():
    data=request.get_json()
    userId=data['userId']
    user = User.query.filter_by(userId=userId).first()
    if user:
        if (user.password!=data['password']):
            return jsonify({"message": "Incorrect password"}), 404
        else:
            return jsonify(user.json())
    return jsonify({"message": "User not found."}), 404

@app.route("/menu")
def getAllMenu():
    return jsonify({"Menu": [menu.json() for menu in Menu.query.all()]})

@app.route("/orderCreate", methods=['POST'])
def order_Create():
    data=request.get_json() 
    """inform restaurant"""
    # default username / password to the borker are both 'guest'
    hostname = "localhost" # default broker hostname. Web management interface default at http://localhost:15672
    port = 5672 # default messaging port.
    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
        # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="order_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')

    # prepare the message body content
    message = json.dumps(data, default=str) # convert a JSON object to a string
    # send the message
    # always inform Monitoring for logging no matter if successful or not
    channel.basic_publish(exchange=exchangename, routing_key="restaurant.info", body=message)
        # By default, the message is "transient" within the broker;
        #  i.e., if the monitoring is offline or the broker cannot match the routing key for the message, the message is lost.
        # If need durability of a message, need to declare the queue in the sender (see sample code below).
    # prepare the channel and send a message to Shipping
    channel.queue_declare(queue='restaurant', durable=True) # make sure the queue used by Shipping exist and durable
    channel.queue_bind(exchange=exchangename, queue='restaurant', routing_key='restaurant.order') # make sure the queue is bound to the exchange
    channel.basic_publish(exchange=exchangename, routing_key="restaurant.order", body=message,
        properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
        )
    )
    print("Order sent to restaurant.")
    # close the connection to the broker
    connection.close()
    return jsonify(message), 201

    

if __name__ == '__main__':
    app.run(port=5001, debug=True)