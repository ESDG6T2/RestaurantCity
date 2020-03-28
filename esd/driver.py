import json
import sys
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pika

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/restaurantdel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)
import requests
getallURL= "http://127.0.0.1:5003/getAllOrders"

class Driver(db.Model):
    __tablename__ = 'driver'
    driverId = db.Column(db.String(45), primary_key=True)
    orderId = db.Column(db.String(45), nullable=False)
    customer_name = db.Column(db.String(45), nullable=False)
    contactNo = db.Column(db.String(45), nullable=False)
    billingAddress = db.Column(db.String(45), nullable=False)
    def __init__(self, driverId, orderId, customer_name, contactNo, billingAddress):
        self.driverId = driverId
        self.orderId = orderId
        self.customer_name = customer_name
        self.contactNo = contactNo
        self.billingAddress = billingAddress

    def json(self):
        return {"driverId":self.driverId,"orderId": self.orderId, "customer_name": self.customer_name, "contactNo": self.contactNo, "billingAddress": self.billingAddress}

@app.route("/getAll")
def getAll():
    # return jsonify("heelo")
    response=requests.get(getallURL)
    msg = json.dumps(response)
    return jsonify(msg)
    # for i in response_dict:
        # print("key: ", i, "val: ", response_dict[i])
    # if r.is_json():
    #     json_data = r.json()
    #     print(json_data)
    # else:
    #     print('yes')

    

@app.route("/driver/<string:driverId>")
#take out the order information and address using driverID.
def find_by_driverID(driverId):
    driver_order_details = Driver.query.filter_by(driverId=driverId).first()
    if driver_order_details:
        return jsonify(driver_order_details.json()), 200
    else:
        return jsonify({'message':'Invalid driver or there is no order assigned'}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5002)


