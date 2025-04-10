from .mock_db import MOCK_DB

def process_refill_logic(data):
    patient_id = data['patient_id']
    rx = data['prescription_number']

    # Mock DB update
    MOCK_DB[patient_id][rx]['refills_left'] -= 1

    return {
        "message": "Refill approved",
        "confirmation": f"REF-{patient_id}-{rx}"
    }
