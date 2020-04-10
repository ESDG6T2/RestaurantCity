import json
import requests
import time
import urllib

TOKEN = '1146167386:AAFuj5hc4FV_YXn1c5Unwtfq-EvqUMC7EEU'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

menuItems = json.loads(requests.get("http://host.docker.internal:5001/menu/").content)['menu']
menuDict = {x['menuId']: x['foodName'] for x in menuItems}

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def handle_updates(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
        except:
            text = update["edited_message"]["text"]
            chat = update["edited_message"]["chat"]["id"]
            
        if text == "/check_status":
            send_message("Please enter your userid starting with @ (e.g. @userid)", chat)
        elif text == "/start":
            send_message("Welcome to Restaurant City", chat)
        elif text[0] == '@':
            reply_msg = 'Dear {}, thank you for choosing Restaurant City. Your order information:\n'.format(text[1:])

            userid = text[1:]
            all_orders = json.loads(requests.get("http://host.docker.internal:8010/order/{}".format(userid)).content)
            all_orders = [order for order in all_orders if order['orderStatus'] != 'delivered' ]
            if len(all_orders) > 1:
                for i, order in enumerate(all_orders):
                    order_info = format_order_info(i+1, order) 
                    reply_msg += order_info  
            else:
                reply_msg = 'Dear {}, you have no orders placed'.format(text[1:])
            send_message(reply_msg, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def format_order_info(idx, order):
    order_info = 'Order {i}:\nDatetime: {datetime}\nStatus: {status}\nOrder items and quantity:\n'.format(i=idx,status=order['orderStatus'],datetime=order['datetime'])
    for i, item in enumerate(order['orderItems']):
        order_info += "{}. {} : {}".format(i+1, menuDict[item['menuId']],item['quantity']) + '\n'
    order_info += '-'*50+'\n'
    return order_info

def main():
    last_update_id = None
    print('Telegram Bot is online')
    while True:
        updates = get_updates(last_update_id)
        try:
            if len(updates["result"]) > 0:
                last_update_id = get_last_update_id(updates) + 1
                handle_updates(updates)        
            time.sleep(0.5)
        except:
            print("Multiple instances running. Please make sure only one instance is running....")

if __name__ == '__main__':
    main()
    
