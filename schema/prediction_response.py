from pydantic import BaseModel , Field
from typing import Dict

class PredictionResponse(BaseModel):
    prediction_category: str = Field(...,description="The predicted Insurance Category",example="High")
    confidence: float = Field(...,description="Model's confidence score for predicted class (range 0 to 1)",example=0.8765)
    class_probabilities: Dict[str,float] = Field(...,description="Probability distribution among all possible clssses",example={"Low":0.1,"Medium":0.15,"High":0.84})