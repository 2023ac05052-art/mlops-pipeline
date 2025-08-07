# validate_data.py
import pandas as pd
from pydantic import BaseModel, ValidationError, Field, TypeAdapter
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

# Use TypeAdapter to validate the entire list of records at once.
list_adapter = TypeAdapter(List[DataSchema])

def validate_data(df: pd.DataFrame):
    """
    Validates a pandas DataFrame against the Pydantic DataSchema
    using a TypeAdapter for efficiency.
    
    Args:
        df: The DataFrame to validate.
        
    Returns:
        A list of validation errors if any, otherwise an empty list.
    """
    try:
        # Convert the DataFrame to a list of dictionaries for validation.
        list_adapter.validate_python(df.to_dict(orient='records'))
        return []
    except ValidationError as e:
        # Pydantic will return all errors in a single ValidationError object.
        return e.errors()

if __name__ == "__main__":
    try:
        # Load your data from the CSV file.
        df = pd.read_csv("data/breast_cancer.csv")
        validation_errors = validate_data(df)

        if validation_errors:
            print("Data validation failed with the following errors:")
            for error in validation_errors:
                print(f"Error: {error}")
            exit(1)
        else:
            print("Data validation successful!")
            exit(0)
    except FileNotFoundError:
        print("Error: 'data/breast_cancer.csv' not found. "
              "Please ensure the file exists.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)
