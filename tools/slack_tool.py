"""
Tool for sharing content to Slack channels.
"""

from langchain.tools import BaseTool
from typing import Dict, Any, Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from langchain_openai import ChatOpenAI
import os
from pydantic import Field

class SlackTool(BaseTool):
    """
    Tool for sharing content to Slack channels.
    """
    
    name = "slack_tool"
    description = """Formats and shares content to Slack channels.
    Use this when the user wants to share insights, analysis, or results to Slack.
    Input should be the content to share or can be empty to share the last message.
    """
    
    llm: Any = Field(default=None, description="Language model to use for content formatting")
    client: Any = Field(default=None, description="Slack API client")
    default_channel: str = Field(default="#product-marketing", description="Default Slack channel to post to")
    
    def __init__(self, llm=None):
        """
        Initialize the Slack tool.
        
        Args:
            llm: Language model to use for content formatting (optional)
        """
        llm = llm or ChatOpenAI(model="gpt-4", temperature=0.5)
        client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
        super().__init__(llm=llm, client=client, default_channel="#product-marketing")
    
    def _run(self, content: Optional[str] = None) -> str:
        """
        Format and share content to Slack.
        
        Args:
            content: The content to share (optional)
            
        Returns:
            Success or error message
        """
        try:
            # If no content provided, try to get the last message from session state
            if not content:
                import streamlit as st
                if "messages" in st.session_state and len(st.session_state.messages) > 0:
                    last_message = st.session_state.messages[-1]["content"]
                    content = last_message
                else:
                    return "No content provided and no previous messages found."
            
            # Format message
            formatted_content = self._format_content(content)
            
            # Share to Slack
            self._share_message(
                formatted_content, 
                self.default_channel
            )
            
            return "Message shared to Slack successfully!"
        except Exception as e:
            return f"Error sharing to Slack: {str(e)}"
    
    def _format_content(self, content: str) -> str:
        """
        Format content for Slack sharing with a routing prompt.
        
        Args:
            content: The content to format
            
        Returns:
            Formatted content
        """
        try:
            # Use LLM to format the content appropriately for Slack
            prompt = f"""You are a professional content formatter for Slack messages.

Task: Format the following content for sharing on Slack.

Content to format:
{content}

Guidelines:
1. Extract the key feature or product name
2. Create a concise, engaging headline
3. Organize the content with appropriate Slack markdown
4. Add relevant emojis to make the message visually appealing
5. Keep the most important insights
6. Format for readability with sections and bullet points
7. Include a brief summary at the top
8. Maximum length: 2000 characters

Output only the formatted Slack message with no additional explanations.
"""
            
            formatted_content = self.llm.invoke(prompt).content
            return formatted_content
        except Exception as e:
            # Fallback to basic formatting
            feature_name = "Product"
            if "our product, " in content:
                feature_name = content.split("our product, ")[1].split(",")[0]
            
            return f"""🚀 *Analysis for {feature_name}*

{content[:1500]}... 

💡 *Shared via Feature Positioning Copilot*"""
    
    def _share_message(self, formatted_content: str, channel: str) -> Dict[str, Any]:
        """
        Share formatted message to Slack.
        
        Args:
            formatted_content: The formatted content to share
            channel: The channel to share to
            
        Returns:
            Slack API response
        """
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=formatted_content,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": formatted_content
                        }
                    }
                ]
            )
            return response
        except SlackApiError as e:
            raise e 