from pydantic import BaseModel
from queue import Queue
from models import PredictTask, PredictInputData, Task
from uuid import uuid4, UUID
from app.src.predict import mock_model_predict
from prediction_results import results_dict

tasks_queue:Queue[PredictTask] = Queue()

def queue_task(task_data: PredictInputData):
    """
    Generates a new task ID, adds a task to the queue, and returns the task ID.

    Args:
        task_data (PredictInputData): The input data for the prediction task.

    Returns:
        str: A unique task ID assigned to the queued task.
    """
    
    # Generating a new uuid
    task_id = str(uuid4())
    print(f"task queued {task_id}")
    results_dict[task_id] = {
        "status": "DONE",
        "task_result": None
    }
    tasks_queue.put(
        PredictTask(
            task_id=task_id,
            task_data=task_data
        )
    )
    return task_id
    

def predict_task_runner():
    """
    Runs the task processing loop, continuously fetching tasks from the queue 
    and processing them.
    """
    print("Task runner started!")
    
    while True:
        task = tasks_queue.get()
        print(f"Starting task :{task.task_id}")
        result = mock_model_predict(task.task_data.input)
        
        results_dict[task.task_id] = {
            "status": "DONE",
            "task_result": {
                "prediction_id": task.task_id,
                "output": result
            }
        }
        print(f"Finished task {task.task_id}")
        tasks_queue.task_done()