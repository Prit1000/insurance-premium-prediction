from fastapi import FastAPI , Path , HTTPException , Query
from fastapi.responses import JSONResponse
from model.predict import MODEL_VIRSON , model_pipeline , predict_output
from schema.user_input import InsuranceData
from schema.prediction_response import PredictionResponse


app = FastAPI()



@app.get("/")
def home():
    return {
        "message": "Insurance Premium Prediction API",
        "version": MODEL_VIRSON,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "model_loaded": model_pipeline is not None ,
        "version": MODEL_VIRSON
    }

@app.post("/predict",response_model=PredictionResponse)
def predict_premium(data: InsuranceData):
    input_dir = {
        "bmi":data.bmi,
        "age_group":data.age_group,
        "lifestyle_risk":data.lifestyle_risk,
        "city_tier":data.city_tier,
        "income_lpa":data.income_lpa,
        "occupation":data.occupation
    }
    try:
        prediction = predict_output(input_dir)   
        return JSONResponse(status_code=200, content={"predicted_category": prediction})
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))
    
    

    