"""
Test cases for tool calling evaluation.
"""

TEST_CASES = [
    {
        "question": "What is the positioning strategy for our new feature?",
        "expected_tool": "positioning_tool",
        "expected_params": {"query": "product positioning statement"}
    },
    {
        "question": "Can you analyze the competitor site at https://example.com?",
        "expected_tool": "scraping_tool",
        "expected_params": {"url": "https://example.com"}
    },
    {
        "question": "Share our latest positioning analysis on Slack",
        "expected_tool": "slack_tool",
        "expected_params": {"content": None}  # Content would be dynamically generated
    }
] 