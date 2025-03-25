import os
from relari_otel import Relari

# Set the environment variable manually
os.environ["RELARI_API_KEY"] = "dummy_key"

# Initialize Relari (without offline=True)
Relari.init(project_name="RefundTest", batch=False)

# Add further agent logic here (mocking refund process)
def process_refund(order_number, reason):
    # Define mock conditions for refund
    if reason.lower() == "damaged":
        return f"Refund processed for order {order_number} due to damaged item."
    elif reason.lower() == "wrong item":
        return f"Refund processed for order {order_number} due to wrong item received."
    else:
        return "Refund request denied."

# Simulate a refund request
order_number = "12345"
reason = "Damaged"
result = process_refund(order_number, reason)

print(result)
