from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/restaurant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

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

    def __init__(self, userId, billingAddress, postalCode,contactNo):
        self.userId = userId
        self.billingAddress = billingAddress
        self.postalCode = postalCode
        self.contactNo = contactNo

    def json(self):
        return {"orderId": self.orderId, "userId": self.userId, "billingAddress": self.billingAddress, "postalCode": self.postalCode, "contactNo": self.contactNo}


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

@app.route("/order", methods=['POST'])
def add_Order():
    data=request.get_json()
    orders = Orders(data['userId'], data['billingAddress'], data['postalCode'],data['contactNo'])
    try:
        db.session.add(orders)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the order."}), 500
    for key, item in data['menuItem'].items():
        orderDetail= OrderDetail(orders.orderId,key,item)
        try:
            db.session.add(orderDetail)
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred creating the order."}), 500

    return jsonify(orders.json()), 201

if __name__ == '__main__':
    app.run(port=5001, debug=True)