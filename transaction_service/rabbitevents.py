from pika import ConnectionParameters, BlockingConnection


class RabbitConnection:
    def __init__(self, properties):
        self.queue = properties['queue']

        connection = BlockingConnection(
            ConnectionParameters(properties['host']))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.queue)


class RabbitProducer(RabbitConnection):
    def __init__(self, properties):
        super().__init__(properties)

        self.exchange = properties['exchange']
        self.channel.exchange_declare(self.exchange, exchange_type='topic')
        self.channel.queue_bind(queue=self.queue, exchange=self.exchange)

    def publish(self, event):
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=self.queue,
                                   body=event)


class RabbitConsumer(RabbitConnection):
    def on_event(self, action):
        def callback(*args):
            action(args)

        self.channel.basic_consume(queue=self.queue,
                                   consumer_callback=callback,
                                   no_ack=True)
        self.channel.start_consuming()
