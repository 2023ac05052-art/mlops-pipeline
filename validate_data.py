# validate_data.py
import pandas as pd
from pydantic import BaseModel, ValidationError, Field
from typing import List

# Define the expected data schema using Pydantic.
# The fields must match the column headers in your CSV file exactly.
# Based on your error message, I've included an example schema
# with column names like 'mean radius'.
class DataSchema(BaseModel):
    # Example fields based on the error message's input_value.
    # You will need to adjust these to match all of your data's columns.
    mean_radius: float = Field(..., alias="mean radius")
    # Add other fields here as needed
    # mean_texture: float = Field(..., alias="mean texture")
    # etc...
    target: int

# A function to perform the validation on a Pandas DataFrame
def validate_data(df: pd.DataFrame):
    """
    Validates a pandas DataFrame against the Pydantic DataSchema.
    
    Args:
        df: The DataFrame to validate.
        
    Returns:
        A list of validation errors if any, otherwise None.
    """
    errors = []
    for index, row in df.iterrows():
        try:
            # Use **row.to_dict() to unpack the row's values into the model constructor.
            # Pydantic will handle the validation.
            DataSchema(**row.to_dict())
        except ValidationError as e:
            # If validation fails, store the error with the row index for better debugging.
            errors.append({"row_index": index, "errors": e.errors()})
    return errors

if __name__ == "__main__":
    # Load your data from the CSV file
    try:

        df = pd.read_csv('data/breast_cancer.csv')

        # Run the validation
        validation_errors = validate_data(df)
        
        if validation_errors:
            print("Data validation failed with the following errors:")
            for error in validation_errors:
                print(f"Row {error['row_index']}: {error['errors']}")
            # Exit with a non-zero status code to fail the GitHub Actions job
            exit(1)
        else:
            print("Data validation successful!")
            # Exit with a zero status code for a successful job
            exit(0)
            
    except FileNotFoundError:
        print("Error: 'csv' not found. Please ensure the file exists.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)
