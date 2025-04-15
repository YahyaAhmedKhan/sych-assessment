from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse
from app.src.predict import mock_model_predict
from models import PredictInputData
from prediction_results import results_dict
from uuid import UUID
from background_task_runner import queue_task, predict_task_runner
import threading, logging, time


# Starting the worker that handles the tasks in the backgroung
threading.Thread(target=predict_task_runner, daemon=True).start()

# Starting the app
app = FastAPI()

# Root route, simple reponse
@app.get("/")
async def root():
    return {"message": "Sych app server running!"}

@app.post("/predict")
async def handle_predict(data: PredictInputData, Async_Mode: str | None = Header(default=None)):
    try: 
        # If async-mode header is true
        if Async_Mode == "true":
            task_id = queue_task(task_data=data)
            return JSONResponse(
                content={
                    "message": "Request received. Processing asynchronously.",
                    "prediction_id": str(task_id)
                },
                status_code=202)
        
        # If async-mode header is not there
        else:
            pred_reuslt = mock_model_predict(data.input)
            return JSONResponse(
                content=pred_reuslt,
                status_code=200)
    except Exception as e:
        return JSONResponse(
            content={
                "error": str(e)
            },
            status_code=500)
        
    

@app.get("/predict/{prediction_id}")
async def get_prediction_task(prediction_id: str):
    
    try:
        # if task id exists
        if task := results_dict.get(prediction_id, None):
            
            # if task is still processing
            if task["status"]=="PROCESSING": # If task not done yet.
                return JSONResponse(
                    content={
                        "error": "Prediction is still being processed."
                    },
                    status_code=400
                )
                
            # if task is done
            elif task["status"]=="DONE": # If task is complete.
                return JSONResponse(
                    content=task["task_result"],
                    status_code=200
                )
                
            # if task status is unrecognzied
            else: 
                raise ValueError(f"Task status unnrecognized: {task['status']}")
        
        # If task id does not exist.
        else:
            return JSONResponse(
                content={
                "error": "Prediction ID not found." 
                },
                status_code=404
            )
    except Exception as e:
        return JSONResponse(
            content={
                "error": str(e)
            },
            status_code=500)