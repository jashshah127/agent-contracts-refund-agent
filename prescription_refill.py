from flask import Flask, request, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class PrescriptionRefillAgent:
    def __init__(self):
        logging.info("Initializing Prescription Refill Agent...")

    def verify_patient_identity(self, patient_id):
        """ Mock function to simulate EHR identity verification """
        ehr_database = {
            "12345": {"name": "John Doe", "dob": "1990-01-01"},
            "67890": {"name": "Jane Smith", "dob": "1985-07-12"}
        }
        return ehr_database.get(patient_id, None)

    def check_prescription_status(self, prescription_number):
        """ Mock function to simulate checking prescription status """
        prescription_database = {
            "RX123": {"status": "refillable", "medication": "XYZ"},
            "RX456": {"status": "expired", "medication": "ABC"},
            "RX789": {"status": "not refillable", "medication": "XYZ"}
        }
        return prescription_database.get(prescription_number, None)

    def check_medication_stock(self, medication_name):
        """ Mock function to simulate checking pharmacy stock """
        stock_database = {
            "XYZ": True,
            "ABC": True,
            "PQR": False
        }
        return stock_database.get(medication_name, False)

    def process_refill_request(self, patient_id, prescription_number, medication_name):
        """ Process the prescription refill request """
        logging.info(f"Processing refill request: {patient_id}, {prescription_number}, {medication_name}")

        # Step 1: Verify patient identity
        patient = self.verify_patient_identity(patient_id)
        if not patient:
            logging.error("Patient identity verification failed.")
            return "Error: Patient identity could not be verified."

        # Step 2: Check prescription status
        prescription = self.check_prescription_status(prescription_number)
        if not prescription:
            logging.error("Prescription not found.")
            return f"Error: Prescription {prescription_number} not found."

        if prescription["status"] != "refillable":
            logging.warning(f"Prescription {prescription_number} is not refillable.")
            return f"Error: Prescription {prescription_number} is not refillable."

        # Step 3: Check medication stock
        in_stock = self.check_medication_stock(medication_name)
        if not in_stock:
            logging.warning(f"Medication {medication_name} is out of stock.")
            return f"Error: Medication {medication_name} is out of stock."

        # If all checks pass, approve refill request
        confirmation_number = f"REF{patient_id[-3:]}{prescription_number[-3:]}"
        logging.info(f"Refill approved. Confirmation Number: {confirmation_number}")
        return f"Refill approved for {patient['name']}. Pickup in 2 hours. Confirmation: {confirmation_number}"

# Initialize Flask app
app = Flask(__name__)
agent = PrescriptionRefillAgent()

@app.route("/process_refill", methods=["POST"])
def process_refill():
    """ API endpoint to process refill requests """
    data = request.json
    patient_id = data.get("patient_id")
    prescription_number = data.get("prescription_number")
    medication_name = data.get("medication_name")

    if not patient_id or not prescription_number or not medication_name:
        return jsonify({"error": "Missing required fields"}), 400

    response = agent.process_refill_request(patient_id, prescription_number, medication_name)
    return jsonify({"message": response})

if __name__ == "__main__":
    app.run(debug=True)
