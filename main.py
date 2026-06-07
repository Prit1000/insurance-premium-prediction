from fastapi import FastAPI , Path , HTTPException , Query
from pydantic import BaseModel , Field , computed_field
from fastapi.responses import JSONResponse
from typing import Annotated , Literal ,Optional
import pandas as pd
import json
import pickle

app = FastAPI()

# import the trained model pipeline
with open("model/model.pkl", "rb") as f:
    # rb means read binary mode, which is necessary for reading a pickle file
    model_pipeline = pickle.load(f)

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata"]
tier_2_cities = ["Pune", "Ahmedabad", "Jaipur", "Lucknow"]    

# pydantic model for the input data
class InsuranceData(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the individual", example=30)]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the individual in kg", example=70.0)]
    height: Annotated[float, Field(..., gt=0, description="Height of the individual in m", example=1.75)]
    income_lpa: Annotated[float, Field(..., gt=0, description="Income of the individual in lakhs per annum", example=5.0)]
    smoker: Annotated[Literal["True", "False"], Field(..., description="Whether the individual is a smoker or not", example="False")]
    city: Annotated[Literal['Kolkata', 'Pune', 'Lucknow', 'Hyderabad', 'Bangalore','Ahmedabad', 'Chennai', 'Mumbai', 'Delhi', 'Jaipur'], Field(..., description="City of residence of the individual", example="Pune")]
    occupation: Annotated[Literal['unemployed', 'salaried_private', 'business_owner', 'retired','government_job', 'student', 'self_employed', 'freelancer'], Field(..., description="Occupation of the individual", example="self_employed")]
    
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi =self.weight / (self.height ** 2)
        return bmi
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
    
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self) ->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

@app.post("/predict")
def predict_premium(data: InsuranceData):
    inupt_df = pd.DataFrame([{
        "bmi":data.bmi,
        "age_group":data.age_group,
        "lifestyle_risk":data.lifestyle_risk,
        "city_tier":data.city_tier,
        "income_lpa":data.income_lpa,
        "occupation":data.occupation
    }])   
    
    prediction = model_pipeline.predict(inupt_df)[0]
    
    return JSONResponse(status_code=200, content={"predicted_category": prediction})

    
    

    