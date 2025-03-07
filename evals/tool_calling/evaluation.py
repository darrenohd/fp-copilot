"""
Evaluation module for tool calling accuracy.
"""
import json
from typing import Dict, List, Any
from langchain_openai import ChatOpenAI

# Import your template
TOOL_CALLING_PROMPT_TEMPLATE = """
You are an evaluation assistant evaluating questions and tool calls to
determine whether the tool called would answer the question. The tool
calls have been generated by a separate agent, and chosen from the list of
tools provided below. It is your job to decide whether that agent chose
the right tool to call.

    [BEGIN DATA]
    ************
    [Question]: {question}
    ************
    [Tool Called]: {tool_call}
    [END DATA]

Your response must be single word, either "correct" or "incorrect",
and should not contain any text or characters aside from that word.
"incorrect" means that the chosen tool would not answer the question,
the tool includes information that is not presented in the question,
or that the tool signature includes parameter values that don't match
the formats specified in the tool signatures below.

"correct" means the correct tool call was chosen, the correct parameters
were extracted from the question, the tool call generated is runnable and correct,
and that no outside information not present in the question was used
in the generated question.

    [Tool Definitions]: {tool_definitions}
"""

class ToolCallingEvaluator:
    """Evaluates tool calling accuracy."""
    
    def __init__(self, model="gpt-4"):
        """Initialize with evaluation model."""
        self.evaluator = ChatOpenAI(model=model, temperature=0)
        
    def format_tool_definitions(self, tools: List[Any]) -> str:
        """Format tool definitions for the prompt."""
        definitions = []
        for tool in tools:
            definitions.append(f"Tool Name: {tool.name}\nDescription: {tool.description}\n")
        return "\n".join(definitions)
        
    def evaluate_tool_call(self, question: str, tool_call: Dict, tool_definitions: List[Any]) -> str:
        """
        Evaluate whether the tool call is correct for the question.
        
        Args:
            question: The user question
            tool_call: The tool call made by the agent
            tool_definitions: List of available tools
            
        Returns:
            "correct" or "incorrect"
        """
        formatted_tool_defs = self.format_tool_definitions(tool_definitions)
        formatted_tool_call = json.dumps(tool_call, indent=2)
        
        prompt = TOOL_CALLING_PROMPT_TEMPLATE.format(
            question=question,
            tool_call=formatted_tool_call,
            tool_definitions=formatted_tool_defs
        )
        
        response = self.evaluator.invoke(prompt)
        result = response.content.strip().lower()
        
        # Validate response is either "correct" or "incorrect"
        if result not in ["correct", "incorrect"]:
            raise ValueError(f"Invalid evaluation result: {result}")
            
        return result 