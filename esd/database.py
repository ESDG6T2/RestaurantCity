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


if __name__ == '__main__':
    app.run(port=5001, debug=True)