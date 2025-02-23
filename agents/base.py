from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from typing import Dict, Any

class BaseAgent(ABC):
    def __init__(self, model: str = "gpt-4", temperature: float = 0.7):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
        
    def _load_prompt_template(self, template_name: str) -> str:
        """Load prompt template from file system"""
        # TODO: Implement prompt template loading from files
        pass

    def _format_prompt(self, template: str, **kwargs) -> str:
        """Format prompt template with variables"""
        return template.format(**kwargs) 