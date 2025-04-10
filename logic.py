from app.contracts import RefillContract
from app.mock_db import MOCK_DB

def process_refill(data):
    contract = RefillContract(data)

    # ✅ Step 1: Check pre-conditions
    if not contract.check_preconditions():
        return {"message": "Preconditions not met.", "errors": contract.get_errors()}, 400

    # ✅ Step 2: Check path conditions
    if not contract.check_path_conditions():
        return {"message": "Path conditions not met.", "errors": contract.get_errors()}, 400

    # ✅ Step 3: Execute business logic
    patient_id = data['patient_id']
    prescription_number = data['prescription_number']
    patient = MOCK_DB.get(patient_id)
    prescription = patient["prescriptions"].get(prescription_number)

    # Fake a refill confirmation
    prescription['last_filled'] = "2025-04-02"
    confirmation_id = f"REF{patient_id[-2:]}{prescription_number[-3:]}"

    # ✅ Step 4: Check post-conditions
    message = f"Refill approved for {patient['name']}. Pickup in 2 hours. Confirmation: {confirmation_id}"
    if not contract.check_postconditions(message):
        return {"message": "Postconditions failed after refill.", "errors": contract.get_errors()}, 500

    return {
        "message": message
    }, 200
