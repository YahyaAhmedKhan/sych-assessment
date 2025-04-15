from fastapi import FastAPI, Header, Request
from mock_model import mock_model_predict
from models import PredictInputData
from prediction_results import results_dict
from uuid import UUID
from background_task_runner import queue_task, predict_task_runner
import threading

threading.Thread(target=predict_task_runner, daemon=True).start()


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict")
async def handle_predict(data: PredictInputData, Async_Mode: str | None = Header(default=None)):
    if Async_Mode:
        task_id = queue_task(task_data=data)
        return {
            "message": "Request received. Processing asynchronously.",
            "prediction_id": str(task_id)
            }
    else:
        return mock_model_predict(data.input)

@app.get("/predict/{prediction_id}")
async def get_prediction_task(prediction_id: str):
    
    task_id_uuid = None
    try:
        task_id_uuid = UUID(prediction_id)
    except:
        return {
            "error": "Prediction ID not found."
            }
    
    if task := results_dict.get(task_id_uuid, None):
        if task["status"]=="PROCESSING": # If task not done yet.
            return {
                "error": "Prediction is still being processed."
            }
        elif task["status"]=="DONE": # If task is complete.
            return task["task_result"]
        else: 
            raise ValueError(f"Task status unnrecognized: {task['status']}")
    else: # Invalid task id.
        return {
            "error": "Prediction ID not found."
            }
