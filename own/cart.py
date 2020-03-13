from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/restaurant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Cart(db.Model):
    __tablename__ = 'temp_cart'
    userid = db.Column(db.String(45), primary_key=True)
    menuId = db.Column(db.String(45), primary_key=True)
    quantity= db.Column(db.Integer, nullable=False)

    def __init__(self,userid, menuId, quantity):
        self.userid = userid
        self.menuId = menuId
        self.quantity = quantity

    def json(self):
        return {"userid":self.userid,"menuId": self.menuId, "quantity": self.quantity}
    

@app.route("/cart/<string:userid>",methods=['GET'])
def get_cart(userid):
    carts = Cart.query.filter_by(userid=userid)
    carts_json = {"cart":[c.json() for c in carts]}

    return jsonify(carts_json), 200

@app.route("/delete-cart/<string:userid>",methods=['GET'])
def delete_cart(userid):
    try:
        Cart.query.filter_by(userid=userid).delete()
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred deleting the cart."}), 500

    return jsonify({"message":"Cart is deleted successfully"}), 200

@app.route("/add-cart/<string:userid>",methods=['POST'])
def create_cart(userid):
    data = request.get_json()

    Cart.query.filter_by(userid=userid).delete()
    db.session.commit()
    
    for item_js in data['items']:
        item = Cart(userid, item_js['menuId'], int(item_js['quantity']))
        try:
            db.session.add(item) # create_cartdb.session object is the current connection of the database 
            db.session.commit() # commit the change to the database 
        except Exception as e:
            print(e)
            return jsonify({"message": "An error occurred saving the cart."}), 500 # INTERNAL SERVER ERROR 
        
    return data, 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True) 