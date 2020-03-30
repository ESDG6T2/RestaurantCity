import pika, os,json

def receiveLog():
    # connect to the broker and set up a communication channel in the connection
    hostname = 'localhost'
    port = 5672
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    channel = connection.channel()

    # set up the exchange with fanout type
    exchange_name = 'info_update'
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue='monitor_info', exclusive=True) # '' indicates a random unique queue name; 'exclusive' indicates the queue is used only by this receiver and will be deleted if the receiver disconnects.
        # If no need durability of the messages, no need durable queues, and can use such temp random queues.
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchange_name, queue=queue_name,routing_key='*.info') # fanout exchange type with no routing keys
        
    # set up a consumer and start to wait for coming messages
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    data = json.loads(body)

    if data['type'] == 'order_receive':
        print("Receive an order:")
        print(data)
    elif data['type'] == 'order_update':
        print("Order updated:")
        print(data)

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("This is " + os.path.basename(__file__) + ": monitoring order creation and feedback submission...")
    receiveLog()
