import pika


class RabbitProducer:
    def __init__(self, queue, exchange):
        self.queue = queue
        self.exchange = exchange
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange, exchange_type='topic')
        self.channel.queue_declare(queue= queue)
        self.channel.queue_bind(queue = queue, exchange = exchange)

    def publish(self, event):
        self.channel.basic_publish(exchange = self.exchange,
                                   routing_key = self.queue,
                                   body = event)

class RabbitConsumer:
    def __init__(self, queue, exchange):
        self.exchange = exchange
        self.queue = queue
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange, exchange_type='topic')
        self.channel.queue_declare(queue= queue)
        self.channel.queue_bind(queue = self.queue, exchange = self.exchange)

    def on_event(self, action):
        def callback(*args):
            action(args)

        self.channel.basic_consume(queue = self.queue,
                                   consumer_callback = callback,
                                   no_ack = True)
        self.channel.start_consuming()
