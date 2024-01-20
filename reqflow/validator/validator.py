from pydantic import BaseModel, ValidationError


class Validator:
    def __init__(self, model: BaseModel):
        self.model = model

    def validate(self, data: dict):
        try:
            # Validate the data using the Pydantic model
            validated_data = self.model.model_validate(data)
            return validated_data
        except ValidationError as e:
            # Handle validation errors
            print("Validation errors:", e.json())
            raise
