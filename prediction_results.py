from uuid import uuid1, UUID
from typing import TypedDict, Literal, Optional
from models import Task    

results_dict: dict[UUID, Task] = {
    
    uuid1(1) : {
        "status": "DONE",
        
        "task_result": {
            "message": "Request received. Processing asynchronously.",
            "prediction_id": "abc123"
            }
    }
}