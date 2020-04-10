from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pika, os, json, pytz
from os import environ

from datetime import datetime

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/restaurantCity_feedback'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("dbURL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

tz = pytz.timezone('Asia/Singapore')

def send_feedback(data):
    hostname = 'rabbitmq'
    port = 5672
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    channel = connection.channel()
    
    message = json.dumps({'star':data['star'],"datetime":data['datetime'],'type':'feedback_receive'}, default=str)
    exchange_name = 'info_update'
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
    channel.basic_publish(exchange=exchange_name, routing_key='feedback.info', body=message)
    print('Feedback sent to monitoring') # for debugging

class Feedback(db.Model):
    __tablename__ = 'feedback'
    datetime = db.Column(db.DateTime, primary_key =True)
    feedback = db.Column(db.String(1000), nullable=False)
    star = db.Column(db.Float(2,1), nullable=False)

    def __init__(self, datetime, feedback, star):
        self.datetime = datetime
        self.feedback = feedback
        self.star = star

    def json(self):
        return {"datetime":self.datetime,"feedback": self.feedback, "star": str(self.star)}

@app.route("/feedback", methods=['POST'])
def create_feedback():
    data = request.get_json()
    feedbackDatetime = datetime.now(tz).strftime(format='%Y-%m-%d %H:%M:%S')
    data['datetime'] = feedbackDatetime
    feedback = Feedback(feedbackDatetime,data['feedback'],data['star'])
    try:
        db.session.add(feedback)
        db.session.commit()
        send_feedback(data)
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred creating the feedback."}), 500

    return jsonify(feedback.json()), 201

@app.route("/getFeedback")
def getAllFeedback():
    return jsonify({"Feedback": [feedback.json() for feedback in Feedback.query.order_by(Feedback.datetime.desc()).all()]})

if __name__ == '__main__':
    app.run(port=5556, debug=True,host='0.0.0.0') 