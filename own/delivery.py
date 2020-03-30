import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/restaurantcity_delivery'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class OrderAllocation(db.Model):
    __tablename__ = 'order_allocation'
    driverId = db.Column(db.String(45), primary_key=True)
    orderId = db.Column(db.String(32), nullable=False)
    customerName = db.Column(db.String(45), nullable=False)
    contactNumber = db.Column(db.String(45), nullable=False)
    deliveryAddress = db.Column(db.String(45), nullable=False)
    
    def __init__(self, driverId, orderId, customerName, contactNumber, deliveryAddress):
        self.driverId = driverId
        self.orderId = orderId
        self.customerName = customerName
        self.contactNumber = contactNumber
        self.deliveryAddress = deliveryAddress

    def json(self):
        return {"driverId":self.driverId,"orderId": self.orderId, "customerName": self.customerName, "contactNumber": self.contactNumber, "deliveryAddress": self.deliveryAddress}

@app.route("/order/<string:driverId>")
#take out the order information and address using driverID.
def find_by_driverID(driverId):
    driver_order_details = Driver.query.filter_by(driverId=driverId).first()
    if driver_order_details:
        return jsonify(driver_order_details.json()), 200
    else:
        return jsonify({'message':'Invalid driver or there is no order assigned'}), 404

@app.route('/allocate-order/<string:orderId>', methods=['POST'])
def allocate_order(orderId):
    data = request.get_json()
    driver_list = [1, 2, 3, 4, 5]  # Assuming 5 drivers
    current_delivery_man = [x['driverId'] for x in OrderAllocation.query.all().json()]
    available = [man for man in driver_list if man not in current_delivery_man]
    orderToAllocate = OrderAllocation(available[0],**data)
    
    try:
        db.session.add(orderToAllocate)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"message": "Error occurred allocating order with id{}.".format(orderId)}), 400
        
    return jsonify(data),201

    
@app.route('/update-delivery/<string:orderId>', methods=['POST'])
# to be used in delivery web UI
def update_order(orderId):
    data = request.get_json()
    try:
        OrderAllocation.query.filter_by(orderId=orderId).update(dict(orderStatus=data['orderStatus'])) # to update a order status
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"message": "Error occurred updating order status of order with id{}.".format(orderId)}), 400
        
    return jsonify(data),201

if __name__ == "__main__":
    app.run(debug=True, port=8000,host='0.0.0.0')


