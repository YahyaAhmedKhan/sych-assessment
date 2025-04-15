import pika
from pika.adapters.blocking_connection import BlockingChannel
from models import PredictInputData, PredictTask
import os


def connect_to_rabbitmq()->BlockingChannel:
    # Connect to RabbitMQ server (localhost if running locally)
    rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')

    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
    channel = connection.channel()

    # Create a queue named 'my_queue'
    channel.queue_declare(queue='sych-app-tasks')
    return channel
        
def add_task_to_rabbitmq(channel:BlockingChannel , task_id:str, task_data:PredictInputData):
    try: 
        task = PredictTask(task_id=task_id, task_data=task_data)
        message = task.model_dump_json()
        print("Adding task: ", message)
        channel.basic_publish(
            exchange="",
            routing_key="sych-app-tasks",
            body=message
        )
    except Exception as e:
        raise RuntimeError(f"Failed to add {task_id} to RabbitMQ")

class RabbitMQConnection:
    """
    A class to get a single RabbbitMQ channel connection. This is meant for all add_task requests.
    The connection for the background task thread uses its own connection.
    """
    _channel: BlockingChannel | None = None

    @classmethod
    def get_channel(cls) -> BlockingChannel:
        if cls._channel is None:
            cls._channel = connect_to_rabbitmq()
        return cls._channel


# add_task_to_rabbitmq(rabbbitMQ_channel, "1", PredictInputData(input="1"))
# add_task_to_rabbitmq(rabbbitMQ_channel, "1", PredictInputData(input="1"))
# add_task_to_rabbitmq(rabbbitMQ_channel, "1", PredictInputData(input="1"))
# add_task_to_rabbitmq(rabbbitMQ_channel, "1", PredictInputData(input="1"))
# add_task_to_rabbitmq(rabbbitMQ_channel, "1", PredictInputData(input="1"))

# import time
# def handles(ch, m, p, body):
#     print(body.decode())
#     time.sleep(0.5)
#     ch.basic_ack(delivery_tag=m.delivery_tag)
    
# rabbbitMQ_channel.basic_qos(prefetch_count=1)
# rabbbitMQ_channel.basic_consume(
#     queue="sych-app-tasks",
#     on_message_callback=handles
# )
# rabbbitMQ_channel.start_consuming()