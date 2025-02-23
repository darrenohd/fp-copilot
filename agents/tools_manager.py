from typing import List, Dict, Callable

class PositioningTools:
    def __init__(self, positioning_agent):
        self.positioning_agent = positioning_agent
        self.available_tools = {
            "analyze_market_fit": {
                "name": "analyze_market_fit",
                "description": "Analyzes market fit based on uploaded documents",
                "func": self.positioning_agent.analyze_market_fit
            },
            "extract_value_props": {
                "name": "extract_value_props",
                "description": "Extracts and analyzes value propositions",
                "func": self.positioning_agent.extract_value_props
            },
            "analyze_competitive_position": {
                "name": "analyze_competitive_position",
                "description": "Analyzes positioning relative to competitors",
                "func": self.positioning_agent.analyze_competitive_position
            },
            "generate_positioning_statement": {
                "name": "generate_positioning_statement",
                "description": "Generates a positioning statement (requires target_segment and key_benefits)",
                "func": self.positioning_agent.generate_positioning_statement
            }
        }
    
    def get_tool_descriptions(self) -> str:
        descriptions = []
        for tool in self.available_tools.values():
            descriptions.append(f"- {tool['name']}: {tool['description']}")
        return "\n".join(descriptions)
    
    def execute_tool(self, tool_name: str, **kwargs):
        if tool_name in self.available_tools:
            return self.available_tools[tool_name]["func"](**kwargs)
        return f"Tool '{tool_name}' not found. Available tools:\n{self.get_tool_descriptions()}" 