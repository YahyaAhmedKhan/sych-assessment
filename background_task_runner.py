from pydantic import BaseModel
from queue import Queue
from models import PredictInputData
from uuid import uuid4, UUID
from mock_model import mock_model_predict
from prediction_results import results_dict

class PredictTask(BaseModel):
    task_id: UUID
    task_data: PredictInputData
    
tasks_queue:Queue[PredictTask] = Queue()

def queue_task(task_data: PredictInputData):
    task_id = uuid4()
    results_dict[task_id] = {
        "status": "DONE",
        "task_result": None
    }
    return task_id
    

def start_predict_task_runner():
    while True:
        task = tasks_queue.get()
        result = mock_model_predict(task.task_data.input)
        results_dict[task.task_id] = {
            "status": "DONE",
            "task_result": result
        }
        
        
        