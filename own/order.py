import pika, os,json,time,requests

# connect to the broker and set up a communication channel in the connection
hostname = 'localhost'
port = 5672
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
channel = connection.channel()

# set up the exchange with fanout type
exchange_name = 'order_direct'
channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

def receiveOrder():
    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue="order", durable=True) # 'durable' makes the queue survive broker restarts so that the messages in it survive broker restarts too
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='order.receive') # bind the queue to the exchange via the key

    # set up a consumer and start to wait for coming messages
    # channel.basic_qos(prefetch_count=1) # The "Quality of Service" setting makes the broker distribute only one message to a consumer if the consumer is available (i.e., having finished processing and acknowledged all previous messages that it receives)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body):  # required signature for the callback; no return
    print("Received an log by " + __file__)
    order = json.loads(body)
    print(order)
    
    # send request to order_flask service to update database
    orderId = order['orderId']
    r = requests.post(url='http://127.0.0.1:6666/add-order/{}'.format(orderId),json=order)
    
    # send to monitoring and notification
    exchange_name = 'info_update'
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
    channel.basic_publish(exchange=exchange_name, routing_key='order.info', body=body)
    
if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("This is " + os.path.basename(__file__) + ": monitoring order creation and feedback submission...")
    receiveOrder()
