
from agent_contracts.contracts import Contract, ContractRegistry

# Define a contract for refund processing
refund_contract = Contract(
    name="RefundProcessingContract",
    preconditions=["User provides order number"],
    pathconditions=["Agent confirms refund eligibility"],
    postconditions=[
        {"on": "output", "value": "Agent outputs refund confirmation message"}
    ]
)

# Register the contract with the system
ContractRegistry.register(refund_contract)
