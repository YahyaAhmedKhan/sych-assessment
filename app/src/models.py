from pydantic import BaseModel
from fastapi import Header
from typing import TypedDict, Literal, Optional
from uuid import UUID
    
class PredictInputData(BaseModel): 
    """
    Model for /predict request body
    """
    input: str
    
class PredictTask(BaseModel):
    """
    A prediction stored in the server's task queue.
    """
    task_id: str
    task_data: PredictInputData
    
class PredictionResult(TypedDict):
    """
    Model prediction model's result dict/json
    """
    input:str
    result:str
    
class PredictionTaskResult(TypedDict):
    """
    Model for /predict/{prediction_id} response
    """
    prediction_id: str
    output: PredictionResult

class TaskResult(TypedDict):
    """
    Model for Task in task queue
    """
    status: Literal["QUEUED", "DONE"]
    task_result: Optional[PredictionTaskResult]
    