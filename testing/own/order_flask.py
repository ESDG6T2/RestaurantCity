from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pika,json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/restaurantcity_order'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

def send_order_status_update(update_info):
    hostname = 'localhost'
    port = 5672
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    channel = connection.channel()

    update_info['type'] = 'order_update'
    message = json.dumps(update_info, default=str)
    
    exchange_name = 'info_update'
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
    channel.basic_publish(exchange=exchange_name, routing_key='order.info', body=message)

class Order(db.Model):
    __tablename__ = 'order'

    orderId = db.Column(db.String(32), primary_key=True)
    userId = db.Column(db.String(45), nullable=False)
    deliveryAddress= db.Column(db.String(45), nullable=False)
    customerName= db.Column(db.String(45), nullable=False)
    contactNumber= db.Column(db.String(45), nullable=False)
    totalAmount=db.Column(db.DECIMAL(5,2), nullable=False)
    orderStatus=db.Column(db.String(10), nullable=True)
    datetime = db.Column(db.DateTime, nullable=False)

    def __init__(self, orderId, userId, deliveryAddress,customerName,contactNumber,totalAmount,orderStatus,orderDatetime):
        self.orderId = orderId
        self.userId = userId
        self.deliveryAddress = deliveryAddress
        self.customerName = customerName
        self.contactNumber = contactNumber
        self.totalAmount=totalAmount
        self.orderStatus = orderStatus
        self.datetime = orderDatetime

    def json(self):
        return {"orderId": self.orderId, "userId": self.userId, "deliveryAddress": self.deliveryAddress, "customerName": self.customerName, "contactNumber": self.contactNumber,
            "totalAmount":self.totalAmount, "orderStatus":self.orderStatus, "datetime":self.datetime
        }

class OrderDetail(db.Model):
    __tablename__ = 'orderdetail'

    orderId = db.Column(db.String(32), primary_key=True)
    menuId = db.Column(db.String(45), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, orderId, menuId, quantity):
        self.orderId = orderId
        self.menuId = menuId
        self.quantity = quantity

    def json(self):
        return {"orderId": self.orderId, "menuId":self.menuId, "quantity":self.quantity}

@app.route('/add-order/<string:orderId>', methods=['POST'])
def add_order(orderId):
    if (Order.query.filter_by(orderId=orderId).first()): # to check if the book is present
        return jsonify({"message": "An Order with order id '{}' already exists.".format(orderId)}), 400
        # 400 is Bad Request

    data = request.get_json()  # use the get_json() is request library to obtain the data passed in with POST
    metadata = {k: v for k, v in data.items() if k != 'orderItems'}
    order = Order(**metadata)  # ** is a common idiom to allow arbitrary number of arguments to a function,
    try:
        db.session.add(order) # db.session object is the current connection of the database 
        db.session.commit() # commit the change to the database 
    except:
        return jsonify({"message": "An error occurred creating the order."}), 500 # INTERNAL SERVER ERROR 

    items = data['orderItems']
    for item in items:
        orderDetail = OrderDetail(data['orderId'], item['sku'],item['quantity'])
        try:
            db.session.add(orderDetail) # db.session object is the current connection of the database 
            db.session.commit() # commit the change to the database 
        except:
            return jsonify({"message": "An error occurred adding the order item."}), 500 # INTERNAL SERVER ERROR 

    return jsonify(order.json()), 201  # CREATED
    
@app.route('/update-order/<string:orderId>', methods=['PUT'])
# to be used in business web UI
def update_order(orderId):
    if not Order.query.filter_by(orderId=orderId).first():
        return jsonify({"message": "No order with id: {}.".format(orderId)}), 400

    data = request.get_json()
    output = {"orderId":orderId,"orderStatus":data['orderStatus']}
    try:
        Order.query.filter_by(orderId=orderId).update(dict(orderStatus=data['orderStatus'])) # to update a order status
        db.session.commit()
        send_order_status_update(output)
    except Exception as e:
        print(e)
        return jsonify({"message": "Error occurred updating order status of order with id: {}.".format(orderId)}), 400
        
    return jsonify(output),201

@app.route('/order/<string:userId>') # complete
def retrieve_order(userId):
    all_orders = [order.json() for order in Order.query.filter_by(userId=userId).order_by(Order.datetime.desc()).all()]
    for order in all_orders:
        items = [item.json() for item in  OrderDetail.query.filter_by(orderId=order['orderId']).all()]
        order['orderItem']= items

    return jsonify(all_orders), 200
    
if __name__ == "__main__":
    app.run(port=6666, host='0.0.0.0', debug=True)