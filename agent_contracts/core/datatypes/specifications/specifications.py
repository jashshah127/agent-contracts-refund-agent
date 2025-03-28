import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field, field_serializer

from agent_contracts.core.utils.nanoid import nanoid

from .contract import Contract


class Scenario(BaseModel):
    uuid: Optional[str] = None
    name: Optional[str] = None
    data: Any
    contracts: List[Contract] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def model_post_init(self, __context: Any):
        if not self.uuid:
            self.uuid = f"con-{nanoid(8)}"

    @field_serializer("contracts")
    def serialize_contracts(self, contracts: List[Contract]):
        return [contract.model_dump() for contract in contracts]

    @staticmethod
    def generate_uuid(data: Any, name: Optional[str] = None):
        try:
            string_repr = str(data).encode()
        except Exception:
            try:
                string_repr = str(data.__dict__).encode()
            except Exception:
                string_repr = str(name).encode() if name else os.urandom(64)
        return f"scene-{hashlib.blake2b(string_repr, digest_size=4).hexdigest()}"

    def get_contract(self, uuid: str):
        for contract in self.contracts:
            if contract.uuid == uuid:
                return contract
        raise KeyError(f"UUID {uuid} not found in scenario")

    @classmethod
    def model_validate(cls, obj: Any, **kwargs) -> "Scenario":
        contracts = [Contract.model_validate(contract) for contract in obj["contracts"]]
        return cls(
            uuid=obj["uuid"],
            name=obj["name"],
            data=obj["data"],
            contracts=contracts,
            metadata=obj.get("metadata", {}),
        )


class Specifications(BaseModel):
    uuid: Optional[str] = None
    scenarios: List[Scenario]

    def __init__(self, scenarios: List[Scenario], uuid: Optional[str] = None, **kwargs):
        if not uuid:
            uuid = nanoid(8)
        super().__init__(scenarios=scenarios, uuid=uuid, **kwargs)

    def model_post_init(self, __context: Any):
        if not self.uuid:
            self.uuid = f"con-{nanoid(8)}"
        uuids = {scenario.uuid for scenario in self.scenarios}
        if len(uuids) != len(self.scenarios):
            raise ValueError("Duplicate UUIDs found in dataset")

    @field_serializer("scenarios")
    def serialize_scenarios(self, scenarios: List[Scenario]):
        return [scenario.model_dump() for scenario in scenarios]

    def __getitem__(self, uuid: str):
        for scenario in self.scenarios:
            if scenario.uuid == uuid:
                return scenario
        raise KeyError(f"UUID {uuid} not found in dataset")

    def __setitem__(self, uuid: str, scenario: Scenario):
        for i, d in enumerate(self.scenarios):
            if d.uuid == uuid:
                self.scenarios[i] = scenario
                return
        self.scenarios.append(scenario)

    def __iter__(self):
        return iter(self.scenarios)

    def __len__(self):
        return len(self.scenarios)

    def __contains__(self, uuid: str):
        return any(scenario.uuid == uuid for scenario in self.scenarios)

    def save(self, path: str):
        path = Path(path)
        dump = self.model_dump()
        if path.suffix == ".json":
            with open(path, "w") as f:
                json.dump(dump, f)
        elif path.suffix == ".yaml":
            with open(path, "w") as f:
                yaml.dump(dump, f, default_flow_style=False, sort_keys=False)
        else:
            raise ValueError(f"Unsupported file extension: {path.suffix}")

    @classmethod
    def load(cls, path: str):
        path = Path(path)
        if path.suffix == ".json":
            data = json.load(open(path, "r"))
            scenarios = [
                Scenario.model_validate(scenario) for scenario in data["scenarios"]
            ]
            return cls(scenarios=scenarios, uuid=data["uuid"])
        elif path.suffix == ".yaml":
            data = yaml.safe_load(open(path, "r"))
            scenarios = [
                Scenario.model_validate(scenario) for scenario in data["scenarios"]
            ]
            return cls(scenarios=scenarios, uuid=data["uuid"])
        else:
            raise ValueError(f"Unsupported file extension: {path.suffix}")
