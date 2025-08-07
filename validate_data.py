# validate_data.py
from pydantic import BaseModel, ValidationError
import pandas as pd

class DataSchema(BaseModel):
    # Define your expected data schema here
    # Example fields:
    feature1: float
    feature2: float
    label: int

# Load your data
try:
    df = pd.read_csv('data/breast_cancer.csv')

    # Iterate through DataFrame rows and validate against the schema
    for _, row in df.iterrows():
        DataSchema(**row.to_dict())
    
    print("Data validation successful!")
except ValidationError as e:
    print("Data validation failed:")
    print(e)
    # You would want to exit with an error code to fail the CI/CD job
    exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)