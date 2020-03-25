from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from random import randint
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/restaurant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class OrderDetail(db.Model):
    __tablename__ = 'orderdetail'

    orderId = db.Column(db.String(45), primary_key=True)
    menuId = db.Column(db.String(45), primary_key=True)
    Qty= db.Column(db.Integer, nullable=False)

    def __init__(self, orderId, menuId, Qty):
        self.orderId = orderId
        self.menuId = menuId
        self.Qty = Qty

    def json(self):
        return {"menuId": self.menuId, "Qty": self.Qty}

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
    driverId=db.Column(db.String(45), nullable=True)

    def __init__(self, userId, billingAddress, postalCode,contactNo,totalAmount):
        self.userId = userId
        self.billingAddress = billingAddress
        self.postalCode = postalCode
        self.contactNo = contactNo
        self.datetime=datetime.now()
        self.totalAmount=totalAmount
        self.orderStatus="Paid"

    def json(self):
        output={"orderId": self.orderId,"userId": self.userId, "billingAddress": self.billingAddress, "postalCode": self.postalCode, "contactNo": self.contactNo, "datetime": self.datetime,"totalAmount": str(self.totalAmount),"orderStatus":self.orderStatus,"driverId":self.driverId}
        output['menuItem']=[orderlist.json() for orderlist in OrderDetail.query.filter_by(orderId=self.orderId).all()] 
        return output


@app.route("/getOrders")
def getAllOrder():
    orders={"orders": [order.json() for order in Orders.query.filter(Orders.orderStatus!="Delivered", Orders.orderStatus!="Delivering").all()]}
    return(orders)

@app.route("/getDeliveryOrders/<string:driverId>", methods=['GEt'])
def getDeliveryOrder(driverId):
    if driverId=='':
        orders={"orders": [order.json() for order in Orders.query.filter(Orders.orderStatus=="Delivering").all()]}
    else:
        orders={"orders": [order.json() for order in Orders.query.filter(Orders.orderStatus=="Delivering", Orders.driverId==driverId).all()]}
    return(orders)

@app.route("/updateOrder", methods=['POST'])
def updateOrder():
    data=request.get_json()
    orderId=data['orderId']
    action=data['action']
        
    order = Orders.query.filter_by(orderId=orderId).first()
    if order:
        try:
            if action=='Delivering':
                driverId=randint(1,4)
                Orders.query.filter_by(orderId=orderId).update({'orderStatus': action, 'driverId':driverId})
            else:
                Orders.query.filter_by(orderId=orderId).update({'orderStatus': action})
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred updating the order."}), 500

        return jsonify(order.json()), 201
    return jsonify({"message": "order not found."}), 404

if __name__ == "__main__":
    app.run(port=5003, debug=True)