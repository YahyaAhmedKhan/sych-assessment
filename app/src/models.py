from pydantic import BaseModel
from fastapi import Header
from typing import TypedDict, Literal, Optional
from uuid import UUID

class PredictInputData(BaseModel): 
    """
    Model for /predict request body
    """
    input: str
    
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
    prediction_id: UUID
    output: PredictionResult

class Task(TypedDict):
    """
    Model for Task in task queue
    """
    status: Literal["PROCESSING", "DONE"]
    task_result: Optional[PredictionTaskResult]
    