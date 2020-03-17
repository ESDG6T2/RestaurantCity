import json
import sys
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pika

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/fill in DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class driver(db.Model):
    __tablename__ = 'order'
    orderID = db.Column(db.Integer, primary_key=True)
    driverID = db.Column(db.String(1000), nullable=False)
    order = db.Column(db.String(1000), nullable=False)
    address = db.Column(db.String(1000), nullable=False)
    def __init__(self, driverID):
        self.orderID = orderID
        self.driverID = driverID
        self.order = order
        self.address = address

    def json(self):
        return {"orderID":self.orderID,"driverID": self.driverID, "order": self.order, "address": self.address}


#take out the order information and address using driverID.
def find_by_driverID(driverID):
    driver_order_details = 


