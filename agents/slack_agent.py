"""
Agent responsible for sharing content to Slack channels.
"""

from .base import BaseAgent
from typing import Dict, Any, Tuple
from utils.tracing import create_span
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

class SlackAgent(BaseAgent):
    """
    Agent responsible for sharing content to Slack channels.
    """
    
    def __init__(self, model="gpt-4", temperature=0.5):
        super().__init__(model, temperature)
        self.client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
        self.default_channel = "#product-marketing"
    
    def execute(self, content: str, channel: str = None) -> Tuple[bool, str]:
        """
        Format and share content to Slack.
        
        Args:
            content: The content to share
            channel: Optional channel override (uses default if not specified)
            
        Returns:
            Tuple of (success, message)
        """
        with create_span("share_to_slack", {
            "channel": channel or self.default_channel,
            "content_length": len(content)
        }) as span:
            try:
                # Extract feature name and format message
                formatted_content = self._format_content(content)
                
                # Share to Slack
                result = self._share_message(
                    formatted_content, 
                    channel or self.default_channel
                )
                
                span.set_attribute("status", "success")
                return True, "Message shared to Slack successfully!"
            except Exception as e:
                span.set_attribute("status", "error")
                span.set_attribute("error_message", str(e))
                return False, f"Error sharing to Slack: {str(e)}"
    
    def _format_content(self, content: str) -> str:
        """
        Format content for Slack sharing with a routing prompt.
        
        Args:
            content: The content to format
            
        Returns:
            Formatted content
        """
        with create_span("format_slack_content") as span:
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
                span.set_attribute("success", True)
                return formatted_content
            except Exception as e:
                span.set_attribute("success", False)
                span.set_attribute("error", str(e))
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
        with create_span("slack_api_call", {"channel": channel}) as span:
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
                span.set_attribute("message_ts", response.get("ts", "unknown"))
                return response
            except SlackApiError as e:
                span.set_attribute("error", str(e))
                raise e 