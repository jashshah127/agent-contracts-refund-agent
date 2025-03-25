import random
import time
import relari
from typing import List
from refund_processing import RefundAgent, refund_contract  # Import the RefundAgent and refund_contract

# Importing Relari and OpenTelemetry packages
from relari.client import RelariClient
from relari_otel.otel import Relari

# Initialize Relari for OpenTelemetry
relari_client = Relari()  # Use Relari class for OpenTelemetry
relari_client.get_trace_id()  # Example usage to get the trace ID for OpenTelemetry

# Main function to simulate refund request
def main():
    print("Welcome to the Refund Processing System")
    
    # Input: Get user order number and refund reason
    order_number = input("Enter your order number: ")
    refund_reason = input("Enter your refund reason (e.g., 'product defect', 'wrong item shipped'): ")
    
    # Initialize Refund Agent
    agent = RefundAgent()

    # Simulate refund processing
    result = agent.process_refund(order_number, refund_reason)
    
    # Output result to user
    print(result)

    # Contract validation (offline verification)
    print("\nVerifying contract...")
    contract = refund_contract()
    
    # Verifying the contract against the agent's actions
    verification_result = contract.verify()  # Adjust based on your actual contract verify method
    if verification_result:
        print("Verification successful! The agent meets the contract conditions.")
    else:
        print("Verification failed! The agent does not meet the contract conditions.")

if __name__ == "__main__":
    main()
