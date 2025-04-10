from enum import Enum
from pathlib import Path

from .prompt_template import PromptTemplate

_DEFAULT_PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts"


class PromptType(Enum):
    SYSTEM = "sys"
    USER = "usr"


class _PromptProvider:
    def __init__(self, base_path: Path = _DEFAULT_PROMPT_PATH):
        if not base_path.exists():
            raise FileNotFoundError(f"Prompt base path {base_path} does not exist")
        self.base_path = base_path
        self.valid_extensions = [".jinja2", ".txt", ".md"]

    def _get_prompt_path(self, name: str, prompt_type: PromptType) -> str:
        for ext in self.valid_extensions:
            fname = f"{name}/{prompt_type.value}{ext}"
            if (self.base_path / fname).exists():
                return self.base_path / fname
        return None

    def get_prompt(self, name: str) -> PromptTemplate:
        return PromptTemplate.from_file(
            system_prompt_path=self._get_prompt_path(name, PromptType.SYSTEM),
            user_prompt_path=self._get_prompt_path(name, PromptType.USER),
        )


PromptProvider = _PromptProvider()
