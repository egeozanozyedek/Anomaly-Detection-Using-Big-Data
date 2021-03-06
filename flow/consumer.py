import socket
import certifi
from confluent_kafka import Consumer, KafkaError
import pickle

class DataConsumer(Consumer):

    def __init__(self, deserializer=pickle.loads, config="local", verbose=True):

        if config is "local":
            conf = {'bootstrap.servers': 'localhost:9092',
                    'group.id': 'mygroup',
                    'enable.auto.commit': True,
                    'default.topic.config': {'auto.offset.reset': 'smallest'}}

        elif config is "cloud":

            conf = {
                'bootstrap.servers': 'pkc-lzvrd.us-west4.gcp.confluent.cloud:9092',
                "security.protocol": "",
                "sasl.mechanisms": "",
                "sasl.username": "PAMBITHEWTHX3PP4",
                "sasl.password": "G8QVRHA85d9yZRt7z2olWWij8MSfVhTxAbxr/pu43YJL6WXQwe0ml5q8JyaVj2w9",
                "security.protocol": "SASL_SSL",
                "sasl.mechanisms": "PLAIN",
                "ssl.ca.location": certifi.where(),
                'group.id': 'mygroup',
                'client.id': 'client-1',
                'enable.auto.commit': True,
                'session.timeout.ms': 6000,
                'default.topic.config': {'auto.offset.reset': 'smallest'}
            }
        else:
            raise Exception("The config option has to be cloud or local")


        super().__init__(conf)
        self.deserializer = deserializer
        self.verbose = verbose

    def stream_data(self, topic=None):

        super().subscribe([topic])
        try:

            while True:

                msg = super().poll(0.1)

                if msg is None:
                    continue

                elif not msg.error():

                    value = self.deserializer(msg.value())
                    if self.verbose:
                        print(f'Received message: {value}')

                    yield value

                elif msg.error().code() == KafkaError._PARTITION_EOF:

                    print('End of partition reached {0}/{1}'
                          .format(msg.topic(), msg.partition()))
                else:

                    print('Error occured: {0}'.format(msg.error().str()))


        except KeyboardInterrupt:
            pass

        finally:
            super().close()


    #
    #
    # def create_batch(self, topic=None, batch_size=64):
