import telegram, json,requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

credential = json.load(open('./data/telebot_credential.json', 'r'))
bot = telegram.Bot(token=credential['token'])

@app.route('/respond', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    msg = update.message.text.encode('utf-8').decode()
    reply_msg = ''
    if text == '/start':  # when user first start the bot
        reply_msg = 'Welcome to Restaurant City'
    elif text == '/check_status':  # when user wanna check the status
        reply_msg = 'Please enter your userid starting with @ (e.g. @userid)'
    elif text[0] == '@':  # when user keys in the userid
        reply_msg = 'The ongoing order information:\n'

        r = requests.get(url='http://127.0.0.1:6666/order/{}'.format(text[1:]))
        
        if r.status_code != 200:
            bot.sendMessage(chat_id=chat_id,text='Sorry, an error occurred. Please try again later.')
            return 'error', 400
        
        all_orders = json.loads(r.content)
        ongoing_orders = [order for order in all_orders if order['status'] != 'delivered'] ## FIXME: if the final status is 'delviered'

        for order in ongoing_orders:
            reply_msg += 'Order id: {orderid}\nDatetime: {datetime}\nOrder items and quantity:\n'.format(orderid=order['orderId'],datetime=order['datetime'])
            order_items = [item.json() for item in OrderDetail.query.filter_by(logId=order['logId']).all()]
            for i,item in enumerate(order_items):
                reply_msg += '{i}.{name}:{quantity}\n'.format(i=i+1, name=menu_items[item['menuId']],quantity=item['quantity'])
            reply_msg += 'order status:{}\n'.format(order['order_status'])
            reply_msg += '-'* 10

    bot.sendMessage(chat_id=chat_id, text=reply_msg)
    return 'success', 200
    
# TODO: set up webhook    
# @app.route('/set_webhook', methods=['GET', 'POST'])
# def set_webhook():
#     s = bot.setWebhook('{URL}{HOOK}'.format(URL='http://0.0.0.0:6000/respond', HOOK=credential['token']))
#     if s:
#         return "webhook setup ok",200
#     else:
#         return "webhook setup failed", 500
        
if __name__ == "__main__":
    r = requests.get(url='http://127.0.0.1:5001/menu')
    menu_items = json.loads(r.content)['menu']
    menu_items = {menu['menuId']:menu['foodName'] for menu in menu_items}
    app.run(port=6000,debug=True,host='0.0.0.0')

