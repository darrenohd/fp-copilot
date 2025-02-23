POSITIONING_ANALYSIS_PROMPT = """You are a senior product marketing strategist with expertise in market positioning and competitive analysis.

Task: Create a comprehensive product positioning analysis for {feature_name}.

Feature Context:
- Feature Name: {feature_name}
- Target Release: {release_date}

Step 1: Analyze the provided information systematically:
Product Information:
{product_info}

User Research:
{user_insights}

Competitive Landscape:
{competitor_info}

[Rest of your existing positioning prompt...]
"""

EXTRACTION_PROMPTS = {
    'name': """Task: Extract the product name from the provided content...""",
    'description': """Task: Create a concise product description...""",
    # Rest of your extraction prompts
} 