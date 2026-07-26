from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import xgboost as xgb
import pandas as pd

app = FastAPI(title="Cyber Threat Classification API", version="1.0")

import os

try:
    model = xgb.XGBClassifier()
    # Get the absolute path to the directory where app.py is located
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, 'xgboost_model.json')
    
    # Load the trained weights into the model shell
    model.load_model(model_path)
    print("Model successfully loaded from disk.")
except Exception as e:
    print(f"Warning: Model not found. Error: {e}")

# Define the data structure we expect from the user/network
class NetworkLog(BaseModel):
    dest_port: int
    packet_size: int
    failed_logins: int
    status_code: int

@app.get("/")
def health_check():
    return {"status": "Secure and Active"}

@app.post("/predict")
def predict_threat(log: NetworkLog):
    try:
        # Convert the incoming JSON payload into a Pandas DataFrame
        data = pd.DataFrame([log.dict()])
        
        # Make a prediction
        prediction = model.predict(data)
        
        # Map the numeric prediction back to our threat labels
        labels = {0: 'Brute_Force', 1: 'DDoS', 2: 'Port_Scan', 3: 'SQL_Injection', 4: 'Safe'}
        predicted_label = labels.get(int(prediction[0]), "Unknown")
        
        return {"prediction": predicted_label, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))