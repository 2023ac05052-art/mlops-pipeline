# validate_data.py
import pandas as pd
from pydantic import BaseModel, ValidationError, Field
from typing import List

# Define the expected data schema using Pydantic.
# The fields must match the column headers in your CSV file exactly.
# This schema now uses aliases that correspond to the abbreviated
# column names in the provided CSV file.
class DataSchema(BaseModel):
    # Use Field(..., alias="column name") for columns with spaces.
    mean_radius: float = Field(..., alias="mean radius")
    mean_texture: float = Field(..., alias="mean textu")
    mean_perimeter: float = Field(..., alias="mean peri")
    mean_area: float = Field(..., alias="mean area")
    mean_smoothness: float = Field(..., alias="mean smoo")
    mean_compactness: float = Field(..., alias="mean com")
    mean_concavity: float = Field(..., alias="mean conc")
    mean_concave_points: float = Field(..., alias="mean conc points")
    mean_symmetry: float = Field(..., alias="mean sym")
    mean_fractal_dimension: float = Field(..., alias="mean fract dim")
    radius_error: float = Field(..., alias="radius err")
    texture_error: float = Field(..., alias="textu err")
    perimeter_error: float = Field(..., alias="peri err")
    area_error: float = Field(..., alias="area err")
    smoothness_error: float = Field(..., alias="smooth err")
    compactness_error: float = Field(..., alias="com err")
    concavity_error: float = Field(..., alias="concav err")
    concave_points_error: float = Field(..., alias="concave points err")
    symmetry_error: float = Field(..., alias="sym err")
    fractal_dimension_error: float = Field(..., alias="fract dim err")
    worst_radius: float = Field(..., alias="worst radius")
    worst_texture: float = Field(..., alias="worst text")
    worst_perimeter: float = Field(..., alias="worst peri")
    worst_area: float = Field(..., alias="worst area")
    worst_smoothness: float = Field(..., alias="worst smoo")
    worst_compactness: float = Field(..., alias="worst com")
    worst_concavity: float = Field(..., alias="worst conc")
    worst_concave_points: float = Field(..., alias="worst conc points")
    worst_symmetry: float = Field(..., alias="worst sym")
    worst_fractal_dimension: float = Field(..., alias="worst fract dim")
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
        # Assuming your data file is named 'data/breast_cancer.csv'
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
        print(f"Error: 'csv' not found. Please ensure the file exists.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)
