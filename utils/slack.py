from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from opentelemetry import trace
from .tracing import create_span

class SlackManager:
    def __init__(self):
        self.client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
        self.channel = "#product-marketing"
    
    def share_message(self, message):
        with create_span("slack_share_message", {
            "channel": self.channel,
            "message_length": len(message)
        }) as span:
            try:
                # Extract feature name from the positioning statement
                feature_name = "Linear"  # Default fallback
                if "our product, " in message:
                    feature_name = message.split("our product, ")[1].split(",")[0]
                    span.set_attribute("feature_name", feature_name)

                # Format the message with markdown and emojis
                formatted_message = f"""🚀 *Product Analysis for {feature_name}*

📊 *Analysis Summary*
💡 *Shared via Feature Positioning Copilot*"""

                response = self.client.chat_postMessage(
                    channel=self.channel,
                    text=formatted_message,
                    blocks=[
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": formatted_message
                            }
                        }
                    ]
                )
                span.set_attribute("status", "success")
                return True, "Message shared to Slack successfully!"
            except SlackApiError as e:
                span.set_attribute("status", "error")
                span.set_attribute("error_message", str(e))
                return False, f"Error sharing to Slack: {str(e)}" 