"""
Agent that routes user requests to appropriate tools.
"""

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from typing import List, Dict, Any
from utils.tracing import initialize_tracer

class RouterAgent:
    """
    Agent responsible for routing user requests to appropriate tools.
    """
    
    def __init__(self, tools, model="gpt-4"):
        """
        Initialize the router agent.
        
        Args:
            tools: List of tools available to the agent
            model: The model to use for the agent
        """
        # Initialize Phoenix tracer in the agent
        self.tracer_provider = initialize_tracer()
        
        self.tools = tools
        
        # Define the prompt template
        system_message = """You are an intelligent AI assistant specializing in product marketing. You have access to several tools:

1. positioning_tool - Use for generating comprehensive product positioning analysis
2. scraping_tool - Use for extracting data from competitor websites (requires a URL)
3. slack_tool - Use for formatting and sharing content to Slack channels
4. rag_tool - Use for answering questions using information from the knowledge base

Your job is to help the user with their product marketing needs by using these tools appropriately.
Always be helpful, professional, and provide concise but complete answers.
"""
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessage(content="{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # Create the agent
        self.llm = ChatOpenAI(model=model, temperature=0.7)
        self.agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def execute(self, user_input: str, chat_history: List = None) -> Dict[str, Any]:
        """
        Execute the agent with user input.
        
        Args:
            user_input: The user's input
            chat_history: Optional chat history for context
            
        Returns:
            Dictionary containing the agent's response and other relevant information
        """
        try:
            if chat_history is None:
                chat_history = []
            
            response = self.agent_executor.invoke({
                "input": user_input,
                "chat_history": chat_history
            })
            
            return {
                "output": response["output"],
                "intermediate_steps": response.get("intermediate_steps", []),
                "success": True
            }
        except Exception as e:
            return {
                "output": f"An error occurred: {str(e)}",
                "success": False
            } 