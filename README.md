# Agent Contracts

![](https://mintlify.s3.us-west-1.amazonaws.com/relari-4243c669/images/verification.svg)

Agent Contracts provide a structured framework for defining, verifying, and certifying the behavior of AI systems. Unlike traditional software, AI-driven systems—especially those powered by large language models (LLMs) and autonomous agents—exhibit probabilistic and emergent behavior, making their correctness hard to define and enforce. Agent Contracts solve this challenge by specifying expected behaviors, constraints, and verification mechanisms in a formal, testable manner.

**Table of Contents**

- [Agent Contracts](#agent-contracts)
  - [Key Components of an Agent Contract](#key-components-of-an-agent-contract)
  - [Why Use Agent Contracts?](#why-use-agent-contracts)
  - [How to use](#how-to-use)
    - [Installation](#installation)
    - [Define your contracts](#define-your-contracts)
    - [Offline Verification](#offline-verification)
    - [Runtime Certification](#runtime-certification)
    - [Anonymous Telemetry](#anonymous-telemetry)
  - [Next Steps](#next-steps)

## Key Components of an Agent Contract

Each Agent Contract consists of three essential components:

1. Preconditions: Conditions that must be met before the agent is executed.
2. Pathconditions: Conditions on the process the agent must follow to achieve the correct outcome.
3. Postconditions: Conditions that must hold after execution.

## Why Use Agent Contracts?

- Formal Verification: Ensure AI agents adhere to expected behaviors, reducing unpredictability
- Automated Testing & Monitoring: Enable systematic validation of AI-generated outputs
- Certifiable AI: Attach verifiable guarantees to AI system decisions for compliance in runtime
- Scalability: Define flexible constraints that generalize across various scenarios and system updates

> [!TIP]
>👉 For more information about agent contracts read the **[whitepaper](https://cdn.prod.website-files.com/669f7329c898141d69e16698/67cf788d56ca9dcf0b88e8d0_1859d1de14107778dccb73c5291f1d5d_Agent%20Contracts%20Whitepaper.pdf) or the [docs](https://agent-contracts.relari.ai/introduction)**.

## How to use

> [!NOTE]
> Javascript/Typescript SDK coming soon!

### Installation

In a folder of your choice cline this repo

```bash
git clone https://github.com/relari-ai/agent-contracts.git
cd agent-contracts
poetry install
```

In your agent application, install the `relari-otel` package to collect traces

```bash
pip install relari-otel[langchain,openai,certification]
```

and instrument your code

```python app.py
from relari_otel.otel import Relari

Relari.init(project_name="Your Project Name")
```

To test the setup is working run your application creating a new trace

```python
with Relari.start_new_sample(scenario_id="scenario_A"):
    await my_agent_code(specs["scenario_A"]["data"])
```

If you run your application and then go to [http://localhost:16686/](http://localhost:16686/), and select `relari-otel` service, you should see the trace of your app.

### Define your contracts

```python
from agent_contracts.core.datatypes.specifications import Contract, Level, Specifications
from agent_contracts.core.verification.pathconditions import Pathcondition
from agent_contracts.core.verification.postconditions import Postcondition
from agent_contracts.core.verification.preconditions import Precondition

## Define the contracts
refund_contract = Contract(
    name="Damaged Item Refund Processing",
    requirements=[
        Precondition("Customer ask for a refund"),
        Precondition("Customer provides order number"),
        Precondition("Customer provides damage description"),
        Pathcondition("Document damage with photos"),
        Pathcondition("Get department manager approval"),
        Postcondition("Send return shipping label", on="output"),
        Postcondition("Provide estimated refund processing time", on="conversation"),
    ],
)

## Define the scenario (collection of contracts)
simple_scenario = Scenario(
    name="Customer Refund Request",
    data={
        "initial_message": "Can I return the sweater I bought last week?",
        ... # other input data to the agentic system in test
    },
    contracts=[refund_contract],
)

## Define the specifications (collection of scenarios)
specs = Specifications(scenarios=[simple_scenario])
# .. and save them to file (json or yaml supported)
specs.save("specs.json")
```

### Offline Verification

In the agent contracts repo, start the verification server

```bash
make docker-verification
```

Run your application through all predefined scenarios

```python
async def runnable(data: Any): # If your agent is not async, you can remove the async and await keywords
    agent_inputs = prepare_my_agent_input(data)
    return my_agent_code(agent_inputs)

await Relari.eval_runner(specs=specs, runnable=runnable) # This will run your application through all predefined scenarios in the specification
```

Once it's done, in the agent contracts repo, first retrieve the run-id

```bash
poetry run cli ls trace --timespan 1h
```

you should see something like

```text
$poetry run cli ls run —timespan 1h
Listing runs from 2025-03-05 21:54:40 to 2025-03-07 21:54:40…
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Run ID   ┃ Project Name        ┃ Specifications ID ┃ Start Time          ┃ End Time            ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ cd26ad7e │ langgraph-fin-agent │ u8spz6vw          │ 2025-03-06 12:45:32 │ 2025-03-06 12:45:32 │
└──────────┴─────────────────────┴───────────────────┴─────────────────────┴─────────────────────┘
```

Then run the verification

```bash
poetry run cli verify run cd26ad7e specs.json --timespan 1h
```

### Runtime Certification

To enable the certification server, we need to change the docker services
If you started the docker services for verification with you need to stop and use instead

```bash
export RUNTIME_VERIFICATION_CONFIG="configs/runtime-certification.yaml" && \
export RUNTIME_VERIFICATION_SPECS="specs.json" && \
make docker-runtime-certification
```

In yout agent code, enable the certification (and make sure you disabled the batching)

```python app.py
from relari_otel.otel import Relari

Relari.init(project_name="Your Project Name", batch=False, certification_enabled=True)
```

Now you can run the certification server

```bash
export RUNTIME_VERIFICATION_CONFIG="configs/runtime-certification.yaml" && \
export RUNTIME_VERIFICATION_SPECS="specs.json" && \
poetry run python3 agent_contracts/certification/runtime_verification.py 
```

In your agent code you can wait for the certificate, for example

```python
async def main():
  with Relari.start_new_sample(scenario_id="my-scenario-id") as sample:
    run_your_code()
    cert = Relari.wait_for_cert()
    print(f"Cert: {cert}")
```

### Anonymous Telemetry

Agent-contracts collects **anonymous** usage statistics.
We receive an event every time a contracts is checked or when the runtime certification is initialized.
This way, we know which components are most relevant to our community.

To opt out of anonymous telemetry set the environment variable `AGENT_CONTRACTS_DO_NOT_TRACK=true`.

## Next Steps

Now that you've created your first contract:

1. Star the repo! ⭐
2. If you have not read already, have a look to the [whitepaper](https://cdn.prod.website-files.com/669f7329c898141d69e16698/67cf788d56ca9dcf0b88e8d0_1859d1de14107778dccb73c5291f1d5d_Agent%20Contracts%20Whitepaper.pdf)
3. Deep dive on how to [defining contracts](https://agent-contracts.relari.ai/contracts/contracts)
4. Understand how to [verify](https://agent-contracts.relari.ai/verification/verification) your agents
5. Read more about [runtime certification](https://agent-contracts.relari.ai/certification/certification)
6. Look at the [examples](https://agent-contracts.relari.ai/examples/finance-agent) in the docs
