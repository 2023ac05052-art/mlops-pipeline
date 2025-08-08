# validate_data.py

import pandas as pd
from pydantic import BaseModel, ValidationError, Field, TypeAdapter
from typing import List


class DataSchema(BaseModel):
    """Schema mapping CSV columns to typed fields."""
    mean_radius: float = Field(..., alias="mean radius")
    mean_texture: float = Field(..., alias="mean texture")
    mean_perimeter: float = Field(..., alias="mean perimeter")
    mean_area: float = Field(..., alias="mean area")
    mean_smoothness: float = Field(..., alias="mean smoothness")
    mean_compactness: float = Field(..., alias="mean compactness")
    mean_concavity: float = Field(..., alias="mean concavity")
    mean_concave_points: float = 
    Field(..., alias="mean concave points")
    mean_symmetry: float = Field(..., alias="mean symmetry")
    mean_fractal_dimension: float = 
    Field(..., alias="mean fractal dimension")
    radius_error: float = Field(..., alias="radius error")
    texture_error: float = Field(..., alias="texture error")
    perimeter_error: float = Field(..., alias="perimeter error")
    area_error: float = Field(..., alias="area error")
    smoothness_error: float = Field(..., alias="smoothness error")
    compactness_error: float = 
    Field(..., alias="compactness error")
    concavity_error: float = Field(..., alias="concavity error")
    concave_points_error: float = 
    Field(..., alias="concave points error")
    symmetry_error: float = Field(..., alias="symmetry error")
    fractal_dimension_error: float = 
    Field(..., alias="fractal dimension error")
    worst_radius: float = Field(..., alias="worst radius")
    worst_texture: float = Field(..., alias="worst texture")
    worst_perimeter: float = Field(..., alias="worst perimeter")
    worst_area: float = Field(..., alias="worst area")
    worst_smoothness: float = Field(..., alias="worst smoothness")
    worst_compactness: float = 
    Field(..., alias="worst compactness")
    worst_concavity: float = Field(..., alias="worst concavity")
    worst_concave_points: float = 
    Field(..., alias="worst concave points")
    worst_symmetry: float = Field(..., alias="worst symmetry")
    worst_fractal_dimension: float = 
    Field(..., alias="worst fractal dimension")
    target: int


list_adapter = TypeAdapter(List[DataSchema])


def validate_data(df: pd.DataFrame):
    """
    Validate a DataFrame against the DataSchema using TypeAdapter.

    Args:
        df: The DataFrame to validate.

    Returns:
        List of validation errors, empty if valid.
    """
    try:
        records = df.to_dict(orient="records")
        list_adapter.validate_python(records)
        return []
    except ValidationError as e:
        return e.errors()


if __name__ == "__main__":
    try:
        df = pd.read_csv("data/breast_cancer.csv")
        validation_errors = validate_data(df)

        if validation_errors:
            print("Data validation failed:")
            for error in validation_errors:
                print(f"Error: {error}")
            exit(1)

        print("Data validation successful!")
        exit(0)

    except FileNotFoundError:
        print(
            "Error: 'data/breast_cancer.csv' not found. "
            "Please ensure the file exists."
        )
        exit(1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)
