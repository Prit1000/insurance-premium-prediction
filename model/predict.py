import pandas as pd
import pickle

# Model virson , usualy count using MLFlow
MODEL_VIRSON = "1.0.0"


# import the trained model pipeline
with open("model/model.pkl", "rb") as f:
    # rb means read binary mode, which is necessary for reading a pickle file
    model_pipeline = pickle.load(f)
    
# get class label from the model (importent for matching prob to class name)
class_label = model_pipeline.classes_.tolist()

def predict_output(user_input:dict):
    user_input_df = pd.DataFrame([user_input])
    
    # predict the class
    predicted_class = model_pipeline.predict(user_input_df)[0]
    
    # get probabilities for all classes
    probabilities = model_pipeline.predict_proba(user_input_df)[0]
    confidence = max(probabilities)
    
    # create mapping: { class name : probabilities}
    class_probs = dict(zip(class_label,map(lambda p: round(p,4), probabilities)))
    return {
        "predicted_category":predicted_class,
        "confidence": confidence,
        "class_probabilities":class_probs
    }
    