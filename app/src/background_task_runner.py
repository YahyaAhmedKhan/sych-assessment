from pydantic import BaseModel
from queue import Queue
from models import PredictTask, PredictInputData, TaskResult
from uuid import uuid4, UUID
from predict import mock_model_predict
from prediction_results import results_dict
from rabbit import add_task_to_rabbitmq, RabbitMQConnection, connect_to_rabbitmq
from pika.adapters.blocking_connection import BlockingChannel
import json

tasks_queue:Queue[PredictTask] = Queue()

def queue_task(task_data: PredictInputData):
    """
    Generates a new task ID, adds a task to the queue, and returns the task ID.

    Args:
        task_data (PredictInputData): The input data for the prediction task.

    Returns:
        str: A unique task ID assigned to the queued task.
    """
    rabbbitMQ_channel = RabbitMQConnection.get_channel()
    
    # Generating a new uuid
    task_id = str(uuid4())
    results_dict[task_id] = {
        "status": "QUEUED",
        "task_result": None
    }
    
    add_task_to_rabbitmq(rabbbitMQ_channel, task_id, task_data)
    print(f"task queued {task_id}")
    return task_id
    
def rabbitmq_task_handler(ch, method, properties, body):
    """
    Callback function to handled consumed message from RabbitMQ
    """
    # Decoded the json from the message and makes a PredictTask object
    
    message_dict = json.loads(body.decode())
    pred_task = PredictTask(**message_dict)
    
    # Processing the task using the mock model
    task_id, task_data = pred_task.task_id, pred_task.task_data
    
    print(f"Started task {task_id} ...")
    pred_result = mock_model_predict(task_data.input)
    results_dict[task_id] = {
        "status": "DONE",
        'task_result': {
            'prediction_id':task_id,
            "output":pred_result
        }
    }
    print(f"Finished task {task_id}\n")
    
    # Acknowledge message to RabbitMQ queue
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
    
def predict_task_runner():
    """
    Runs the task processing loop, continuously fetching tasks from the queue 
    and processing them.
    """
    print("Task runner with RabbitMQ started!\n")
    
    # Separate channel connection for this as it runs on a background thread and pika is not thread safe.
    # So I couldn't use the same connection channel for both.
    rabbbitMQ_channel = connect_to_rabbitmq()
    rabbbitMQ_channel.basic_qos(prefetch_count=1)
    
    # Defining the consume callback
    rabbbitMQ_channel.basic_consume(
        queue="sych-app-tasks",
        on_message_callback=rabbitmq_task_handler # This function runs evrytime a message is read from the quque
    )
    
    rabbbitMQ_channel.start_consuming()