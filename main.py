from fastapi import FastAPI, Header, Request
from mock_model import mock_model_predict
from models import PredictInputData
from prediction_results import results_dict
from uuid import UUID

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict")
async def handle_predict(data: PredictInputData, Async_Mode: str | None = Header(default=None)):
    if Async_Mode:
        pass
    
    else:
        return mock_model_predict(data.input)

@app.get("/predict/{prediction_id}")
async def get_prediction_task(prediction_id: str):
    try:
        pass
    except:
        return 
    
    if task := results_dict.get(UUID(prediction_id), None):
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
