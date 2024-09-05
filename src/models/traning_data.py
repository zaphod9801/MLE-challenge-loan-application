from pydantic import BaseModel
from typing import List

class TrainingData(BaseModel):
    Age: List[float]
    Annual_Income: List[float]
    Credit_Score: List[float]
    Loan_Amount: List[float]
    Number_of_Open_Accounts: List[float]
    Had_Past_Default: List[int]
    Loan_Duration_Years: List[int]
    Loan_Approval: List[int]