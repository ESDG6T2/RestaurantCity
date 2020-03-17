import json
import sys
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    orderID = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.String(1000), nullable=False)
    star = db.Column(db.String(1), nullable=False)

    def __init__(self, feedback, star):
        self.feedback = feedback
        self.star = star

    def json(self):
        return {"orderID":self.orderID,"feedback": self.feedback, "star": self.star}

    

@app.route("/Feedback", methods=['POST'])
#create feedback in the DB
def create_feedback():

    data = request.get_json()
    feedback = Feedback(data['feedback'],data['star'])
    
    try:
        db.session.add(feedback)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the feedback."}), 500

    return jsonify(feedback.json()), 201


@app.route('/')
def index():
    return render_template('Feedback.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True) 