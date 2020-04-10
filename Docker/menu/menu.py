from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("dbURL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Menu(db.Model):
    __tablename__ = 'Menu'

    menuId = db.Column(db.String(45), primary_key=True)
    foodName = db.Column(db.String(45), nullable=False)
    price= db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, menuId, foodName, price):
        self.menuId = menuId
        self.foodName = foodName
        self.price = price

    def json(self):
        return {"menuId": self.menuId, "foodName": self.foodName, "price": self.price}


@app.route("/menu/")
def getAllMenu():
    return jsonify({"menu": [menu.json() for menu in Menu.query.all()]})

@app.route("/menu-item/<string:menuId>")
def get_item(menuId):
    item = Menu.query.filter_by(menuId=menuId).first()

    if item:
        return jsonify(item.json()), 200
    else:
        return jsonify({'message':'Menu item not found'}),404

if __name__ == "__main__":
    app.run(debug=True,port=5001,host='0.0.0.0')