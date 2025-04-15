import time
import random
from models import PredictionResult

def mock_model_predict(input: str) -> PredictionResult: 
    time.sleep(random.randint(10, 17)) # Simulate processing delay
    # time.sleep(random.randint(10, 17)) # Simulate processing delay
    result = str(random.randint(1000, 20000))
    output:PredictionResult = {"input": input, "result": result}
    return output
