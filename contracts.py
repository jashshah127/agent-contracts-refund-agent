from pydantic import BaseModel, ValidationError
from .mock_db import MOCK_DB

class RefillInput(BaseModel):
    patient_id: str
    prescription_number: str
    medication_name: str

class RefillContract:
    def __init__(self, data):
        self.data = data
        self.errors = []

    def check_preconditions(self):
        try:
            RefillInput(**self.data)  # Validates schema
            return True
        except ValidationError as e:
            self.errors.append(str(e))
            return False

    def check_path_conditions(self):
        # Example path logic (you can expand this)
        if self.data.get("medication_name") not in ["XYZ", "ABC", "123"]:
            self.errors.append("Medication not supported")
        return not self.errors

    def check_postconditions(self, response_message):
        # Example post-condition check (can be customized)
        if "Refill approved" not in response_message:
            self.errors.append("Postcondition failed: Refill not approved")
        return not self.errors

    def get_errors(self):
        return self.errors
