from uuid import uuid1, UUID
from typing import TypedDict, Literal, Optional
from models import Task    

results_dict: dict[UUID, Task] = {
    
    uuid1(1) : {
        "status": "DONE",
        
        "task_result": {
            "prediction_id": "abc123",
            "output": {"input": "Sample input data for the model", "result": "5678"} 
            }
    }
}