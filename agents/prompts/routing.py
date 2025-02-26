"""
Prompt templates for routing user requests to appropriate agents.
"""

AGENT_ROUTING_PROMPT = """You are an intelligent routing system for a product marketing assistant.

Available tools:
1. PositioningAgent - Generates comprehensive product positioning analysis
2. ScrapingAgent - Extracts structured data from competitor websites
3. SlackAgent - Formats and shares content to Slack channels
4. RAG - Retrieves information from the knowledge base to answer questions

User request: {user_request}

Determine which tool would be most appropriate to handle this request.
Consider:
- Requests about "positioning", "analysis", or "strategy" should use PositioningAgent
- Requests to "analyze", "scrape", or "extract" from websites should use ScrapingAgent
- Requests to "share", "post", or "send to slack" should use SlackAgent
- General questions should use RAG

Output only the name of the appropriate tool: "PositioningAgent", "ScrapingAgent", "SlackAgent", or "RAG"
""" 