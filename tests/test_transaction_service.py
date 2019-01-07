
# import mock

# from transaction_service import consume


# @mock.patch('pika.BlockingConnection')
# def test_channel(channel):
#     assert channel() != None

# def test_message_consumer(channel):
#     channel.basic_publish(exchange='',
#                           routing_key='hello',
#                           body='Hello World!')

#     def callback(ch, method, properties, body):
#         print(body)
#     consume(channel, callback)

