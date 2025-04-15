from rabbit import add_task_to_rabbitmq, RabbitMQConnection, connect_to_rabbitmq
from models import PredictInputData


# rabbbitMQ_channel = RabbitMQConnection.get_channel()
# add_task_to_rabbitmq(rabbbitMQ_channel, "3", PredictInputData(input="1"))

# rabbbitMQ_channel = RabbitMQConnection.get_channel()
# add_task_to_rabbitmq(rabbbitMQ_channel, "2", PredictInputData(input="1"))

# rabbbitMQ_channel = RabbitMQConnection.get_channel()
# rabbbitMQ_channel = RabbitMQConnection.get_channel()

# channel = connect_to_rabbitmq()

# add_task_to_rabbitmq(rabbbitMQ_channel, "2", PredictInputData(input="1"))
# add_task_to_rabbitmq(rabbbitMQ_channel, "2", PredictInputData(input="1"))
# add_task_to_rabbitmq(rabbbitMQ_channel, "2", PredictInputData(input="1"))
# add_task_to_rabbitmq(rabbbitMQ_channel, "2", PredictInputData(input="1"))
# add_task_to_rabbitmq(rabbbitMQ_channel, "2", PredictInputData(input="1"))

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




add_task_to_rabbitmq(RabbitMQConnection.get_channel(), "1", PredictInputData(input="1"))
