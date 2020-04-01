from flask import Flask, render_template, jsonify, request
import paypalrestsdk
import json
from urllib.parse import unquote
# from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AdYNpArZeEoIQS7QUQk4BfO5HbY3I5ppd7ttEK1aimWGDIdywW1CWWBZ_1tR5JEm4vg5UMpP9lkaKPVK",
  "client_secret": "EFk8M9WgnCn5OBJaGiqEskzGcPZaUiqmP8-zKyHx7PGxdvZyze4FuHKg2jjCPJBp2MzSvUiOjc8BqmqX" })

@app.route('/checkout', methods=['GET', 'POST'])
def index():
    # data=request.args
    url = request.url
    cut_index=url.find('?')
    url = url[cut_index+1:]
    data = unquote(unquote(url))
    parsed = json.loads(data)
    # return json.dumps(parsed, indent=4)
    # return parsed
    return render_template('index.html', data=parsed)

@app.route('/payment', methods=['POST'])
def payment():
    # order_data = request.form.to_dict()
    orderItems = json.loads(request.form['orderitems'])
    price = request.form['price']
    # print(orderItems[1])
    orderItemsList = []
    for i in range(len(orderItems)):
        orderItemsDict = {
            "sku" : orderItems[i]['sku'],
            "name" : orderItems[i]['name'],
            "price" : orderItems[i]['price'],
            "currency" : "SGD", 
            "quantity" : orderItems[i]['quantity']
        }
        orderItemsList.append(orderItemsDict)
        orderItemsDict = {}
    
    # order_data = ImmutableMultiDict(order_data)
    # order_data.to_dict()
    # print(order_data['orderItems'])
    # print(str(orderItemsList))
    # print(str(price)+'.00')
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{ # TODO: need to input item list: get from BODY
            "item_list": {
                "items": orderItemsList},
            "amount": { # TODO: need to input Total Amount
                "total": str(price),
                "currency": "SGD"},
            "description": "This is the payment transaction description."}]}) # TODO: need to input decription

    if payment.create():
        print('Payment create success!')
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


    # payment = paypalrestsdk.Payment({
    #     "intent": "sale",
    #     "payer": {
    #         "payment_method": "paypal"},
    #     "redirect_urls": {
    #         "return_url": "http://localhost:3000/payment/execute",
    #         "cancel_url": "http://localhost:3000/"},
    #     "transactions": [{ # TODO: need to input item list: get from BODY
    #         "item_list": {
    #             "items": [{
    #                 "sku": "F01",
    #                 "name": "Bola Obi",
    #                 "price": "10.00",
    #                 "currency": "SGD",
    #                 "quantity": 1}]},
    #         "amount": { # TODO: need to input Total Amount
    #             "total": "10.00",
    #             "currency": "SGD"},
    #         "description": "This is the payment transaction description."}]}) # TODO: need to input decription
