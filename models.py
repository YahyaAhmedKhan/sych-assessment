from pydantic import BaseModel
from fastapi import Header
from typing import TypedDict, Literal, Optional

class PredictInputData(BaseModel):
    input: str

class TaskResult(TypedDict):
    message: str
    prediction_id: str 

class Task(TypedDict):
    status: Literal["PROCESSING", "DONE"]
    task_result: Optional[TaskResult]
    