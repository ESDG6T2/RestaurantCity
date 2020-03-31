from flask import Flask, render_template, jsonify, request
import paypalrestsdk

app = Flask(__name__)

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AdYNpArZeEoIQS7QUQk4BfO5HbY3I5ppd7ttEK1aimWGDIdywW1CWWBZ_1tR5JEm4vg5UMpP9lkaKPVK",
  "client_secret": "EFk8M9WgnCn5OBJaGiqEskzGcPZaUiqmP8-zKyHx7PGxdvZyze4FuHKg2jjCPJBp2MzSvUiOjc8BqmqX" })

@app.route('/checkout',methods=['POST'])
def index():
    return render_template('index.html')

@app.route('/payment', methods=['POST'])
def payment():

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{ # TODO: need to input item list: get from BODY
            "item_list": {
                "items": [{
                    "sku": "F01",
                    "name": "Bola Obi",
                    "price": "10.00",
                    "currency": "SGD",
                    "quantity": 1}]},
            "amount": { # TODO: need to input Total Amount
                "total": "10.00",
                "currency": "SGD"},
            "description": "This is the payment transaction description."}]}) # TODO: need to input decription

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success' : success})

if __name__ == '__main__':
    app.run(port=7000, host='0.0.0.0', debug=True)