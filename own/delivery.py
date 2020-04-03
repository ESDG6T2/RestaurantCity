import json,pika
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/restaurantcity_order'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

def send_delivery_allocation(update_info):
    hostname = 'localhost'
    port = 5672
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    channel = connection.channel()

    update_info['type'] = 'order_deliver'
    message = json.dumps(update_info, default=str)
    
    exchange_name = 'info_update'
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
    channel.basic_publish(exchange=exchange_name, routing_key='delivery.info', body=message)

class OrderAllocation(db.Model):
    __tablename__ = 'order'
    orderId = db.Column(db.String(32), primary_key=True)
    driverId = db.Column(db.String(45), nullable=True)
    customerName = db.Column(db.String(45), nullable=False)
    contactNumber = db.Column(db.String(45), nullable=False)
    deliveryAddress = db.Column(db.String(45), nullable=False)
    orderStatus = db.Column(db.String(45),nullable=False)

    def __init__(self, driverId, orderId, customerName, contactNumber, deliveryAddress,orderStatus):
        self.driverId = driverId
        self.orderId = orderId
        self.customerName = customerName
        self.contactNumber = contactNumber
        self.deliveryAddress = deliveryAddress
        self.orderStatus = orderStatus

    def json(self):
        return {"driverId": self.driverId, "orderId": self.orderId, "customerName": self.customerName, "contactNumber": self.contactNumber, "deliveryAddress": self.deliveryAddress,
            'orderStatus':self.orderStatus
        }

@app.route("/order/<string:driverId>")
#take out the order information and address using driverID.
def find_by_driverID(driverId):
    if driverId in ['1', '2', '3', '4', '5']:
        driver_order_details = OrderAllocation.query.filter(OrderAllocation.driverId==driverId, OrderAllocation.orderStatus!='delivered').first()
        if driver_order_details:
            return jsonify(driver_order_details.json()), 200
        else:
            return jsonify({'message': 'There is no order assigned'}), 400

    return jsonify({'message': 'Invalid driver ID'}), 400

@app.route('/allocate-order/<string:orderId>', methods=['PUT'])
def allocate_order(orderId):
    if not OrderAllocation.query.filter_by(orderId=orderId).first():
        return jsonify({"message": "No order with id: {}.".format(orderId)}), 400
    else:
        order = OrderAllocation.query.filter_by(orderId=orderId).first().json()
        driverId = order['driverId']
        if driverId:
            return jsonify({"message": "Order {} has been assigned to driver {} for delivery.".format(orderId,driverId)}), 400

    driver_list = ['1', '2', '3', '4',' 5']  # Assuming 5 drivers
    delivering_orders = [x.json() for x in OrderAllocation.query.filter_by(orderStatus='delivering').all()]
    
    delivering_man = [x['driverId'] for x in delivering_orders]
    available = [man for man in driver_list if man not in delivering_man]

    if available == []:
        return jsonify({"message": "No available drivers. Please wait for drivers to return"}), 400
    to_delivery = available[0]
    
    try:
        OrderAllocation.query.filter_by(orderId=orderId).update(dict(driverId=to_delivery)) # to update a order status
        db.session.commit()
        send_delivery_allocation({"orderId":orderId,"deliveryMan":to_delivery})
    except Exception as e:
        print(e)
        return jsonify({"message": "Error occurred allocating order with id: {}.".format(orderId)}), 400
        
    return jsonify({"orderId":orderId,"driverId":to_delivery}),200

if __name__ == "__main__":
    app.run(debug=True, port=8000,host='0.0.0.0')


