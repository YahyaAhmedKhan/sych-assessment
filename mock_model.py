import time
import random
from typing import Dict
from 

def mock_model_predict(input: str) -> :
    time.sleep(random.randint(2, 3)) # Simulate processing delay
    # time.sleep(random.randint(10, 17)) # Simulate processing delay
    result = str(random.randint(1000, 20000))
    output = {"input": input, "result": result}
    return output
