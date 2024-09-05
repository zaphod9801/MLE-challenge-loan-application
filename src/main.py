import os
from fastapi import FastAPI
from typing import List
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from dotenv import load_dotenv
from src.models.loan_application import LoanApplication
from src.models.traning_data import TrainingData

load_dotenv()

app = FastAPI()

model = None
X_train, X_test, y_train, y_test = None, None, None, None

DATASET_PATH = os.getenv("DATASET_PATH")

if not DATASET_PATH:
    raise EnvironmentError("The DATASET_PATH environment variable is not set.")


def train_model():
    """
    The `train_model` function reads a dataset, imputes missing values, splits the data into training
    and testing sets, and trains a logistic regression model for loan approval prediction.
    
    Returns:
      "Model retrained successfully"
    """
    global model, X_train, X_test, y_train, y_test
    
    df = pd.read_csv(DATASET_PATH)

    imputer = SimpleImputer(fill_value=0)
    df_imputed = df.copy()
    df_imputed[['Age', 'Annual_Income', 'Credit_Score', 'Loan_Amount', 'Number_of_Open_Accounts', 'Had_Past_Default', 'Loan_Duration_Years']] = imputer.fit_transform(
        df[['Age', 'Annual_Income', 'Credit_Score', 'Loan_Amount', 'Number_of_Open_Accounts', 'Had_Past_Default', 'Loan_Duration_Years']]
    )
    df_imputed.drop('Unnamed: 0', axis=1, inplace=True)

    X = df_imputed.drop('Loan_Approval', axis=1)
    y = df_imputed['Loan_Approval']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    return "Model retrained successfully"
    
    
# Endpoint /health
@app.get("/health")
async def health_check():
    """
    The `health_check` function returns a dictionary with the status "healthy".
    
    Returns:
      A dictionary with the key "status" and the value "healthy" is being returned.
    """
    return {"status": "healthy"}
    
    
@app.post("/predict")
async def predict_loan_approval(applicant: LoanApplication):
    """
    The function `predict_loan_approval` takes in a `LoanApplication` object, makes a prediction using a
    pre-trained model, and returns the loan approval prediction as an integer.
    
    Args:
      applicant (LoanApplication): The `applicant` parameter in the `predict_loan_approval` function
    represents a `LoanApplication` object that contains the details of a loan applicant. This object is
    expected to be passed in the POST request to the `/predict` endpoint. The function creates a pandas
    DataFrame from the applicant data, makes a prediction using the dataframe.
    
    Returns:
      The code is returning a JSON response with the key "Loan_Approval_Prediction" and the predicted
    loan approval value as the corresponding integer value.
    """
    data = pd.DataFrame([applicant.dict()])
    prediction = model.predict(data)

    return {"Loan_Approval_Prediction": int(prediction[0])}
    
@app.post("/retrain")
async def retrain_model():
    """
    The `retrain_model` function asynchronously retrains a model and returns a message indicating the
    result.
    
    Returns:
      The function `retrain_model` is an asynchronous function that calls the `train_model` function and
    assigns the result to the variable `message`. It then returns a dictionary with a key "message"
    containing the value of the `message` variable.
    """
    message = train_model()

    return {"message": message}
    
def load_and_train_initial_model():
    """
    The function `load_and_train_initial_model` loads and trains an initial model.
    """
    train_model()

load_and_train_initial_model()
