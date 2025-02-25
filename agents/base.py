"""
Base agent class for all agents in the Feature Positioning Copilot.
"""

from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from typing import Dict, Any, Optional
from utils.tracing import create_span

class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.
    
    Provides common functionality for LLM interaction, prompt formatting,
    and error handling.
    """
    
    def __init__(self, model: str = "gpt-4", temperature: float = 0.7):
        """
        Initialize the base agent.
        
        Args:
            model: The LLM model to use
            temperature: The temperature parameter for the LLM
        """
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        
    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Execute the agent's primary function.
        
        This method must be implemented by all subclasses.
        """
        pass
        
    def _load_prompt_template(self, template_name: str) -> str:
        """
        Load prompt template from file system.
        
        Args:
            template_name: Name of the template to load
            
        Returns:
            The loaded template as a string
        """
        # TODO: Implement prompt template loading from files
        raise NotImplementedError("Prompt template loading not implemented yet")

    def _format_prompt(self, template: str, **kwargs) -> str:
        """
        Format prompt template with variables.
        
        Args:
            template: The template string to format
            **kwargs: Variables to insert into the template
            
        Returns:
            The formatted prompt string
        """
        with create_span("format_prompt", {"template_length": len(template)}) as span:
            try:
                result = template.format(**kwargs)
                span.set_attribute("success", True)
                return result
            except Exception as e:
                span.set_attribute("success", False)
                span.set_attribute("error", str(e))
                raise
                
    def _handle_error(self, error_message: str) -> None:
        """
        Handle errors in agent execution.
        
        Args:
            error_message: The error message to log
        """
        with create_span("agent_error", {"message": error_message}) as span:
            # In a real implementation, this would log to a proper logging system
            print(f"Agent error: {error_message}")
            span.set_attribute("error", error_message) 