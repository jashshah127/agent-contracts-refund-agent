import random

class RefundAgent:
    def __init__(self):
        self.name = "RefundAgent"
        print(f"Initializing {self.name}")

    def process_refund(self, order_number: str, refund_reason: str) -> str:
        """
        Process the refund based on eligibility.
        :param order_number: The order number for the refund request.
        :param refund_reason: The reason for the refund request.
        :return: Refund status message.
        """
        print(f"Processing refund for order {order_number} due to: {refund_reason}")
        
        # Simulating refund eligibility check (random logic)
        eligible_reasons = ["product defect", "wrong item shipped", "item not received"]
        if refund_reason.lower() in eligible_reasons:
            return self.issue_refund(order_number, refund_reason)
        else:
            return self.deny_refund(order_number, refund_reason)

    def issue_refund(self, order_number: str, refund_reason: str) -> str:
        """
        Issue the refund confirmation.
        :param order_number: The order number being refunded.
        :param refund_reason: The reason for the refund.
        :return: Confirmation message.
        """
        confirmation_number = random.randint(1000, 9999)
        return f"Refund for order {order_number} due to {refund_reason} has been approved. Confirmation #: {confirmation_number}"

    def deny_refund(self, order_number: str, refund_reason: str) -> str:
        """
        Deny the refund and give a reason.
        :param order_number: The order number.
        :param refund_reason: The reason for the denial.
        :return: Denial message.
        """
        return f"Refund request for order {order_number} due to {refund_reason} is denied. Reason: Not eligible for refund."


# Example contract for refund processing
class Contract:
    def __init__(self, precondition, pathcondition, postcondition):
        self.precondition = precondition
        self.pathcondition = pathcondition
        self.postcondition = postcondition

    def verify(self):
        """
        Basic contract verification logic.
        Here, we're just checking if the conditions are met.
        This can be extended based on your business rules.
        """
        if self.precondition and self.pathcondition and self.postcondition:
            print("Contract verification passed.")
            return True
        else:
            print("Contract verification failed.")
            return False


# Function to create a contract for refund processing
def refund_contract():
    contract = Contract(
        precondition="User provides valid order number",
        pathcondition="Agent confirms refund eligibility based on reasons",
        postcondition="Agent outputs refund confirmation or denial message"
    )
    return contract
