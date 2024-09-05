from pydantic import BaseModel

# This class represents a loan application with attributes such as age, annual income, credit score,
# loan amount, loan duration in years, number of open accounts, and a flag indicating past default
# history.
class LoanApplication(BaseModel):
    Age: float
    Annual_Income: float
    Credit_Score: float
    Loan_Amount: float
    Loan_Duration_Years: int
    Number_of_Open_Accounts: float
    Had_Past_Default: int
    