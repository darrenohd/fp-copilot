"""
Prompt templates for extraction tasks.
"""

EXTRACTION_PROMPTS = {
    'name': """Task: Extract the product name from the provided content.
    
    Context: You are analyzing a product webpage to identify the official product name.
    
    Instructions:
    1. Look for the main product title or heading
    2. Ignore marketing taglines or slogans
    3. Return only the core product name
    4. If multiple versions exist, return the primary/latest version
    
    Content: {text}
    
    Product name:""",
    
    'description': """Task: Create a concise product description.
    
    Context: You are analyzing a product webpage to create a clear, benefit-focused description.
    
    Instructions using Tree of Thoughts:
    1. Core Function
       - What is the primary purpose of the product?
       - What problem does it solve?
    
    2. Key Benefits
       - What are the main advantages?
       - How does it improve the user's life?
    
    3. Unique Features
       - What distinguishes it from alternatives?
       - What innovative capabilities does it offer?
    
    Synthesize these points into a clear, concise description (max 2 sentences).
    
    Content: {text}
    
    Description:""",
    
    'pain_points': """Task: Identify the top 3 customer problems this product solves.
    
    Context: You are analyzing product marketing content to understand customer pain points.
    
    Using Zero-Shot Chain-of-Thought:
    1. First, let's identify all mentioned customer challenges
    2. Then, analyze which problems are emphasized most
    3. Finally, select the top 3 based on:
       - Frequency of mention
       - Emphasis in marketing
       - Severity of the problem
       - Clarity of the solution
    
    Content: {text}
    
    Output the top 3 pain points in a comma-separated list:""",
    
    'pricing': """Task: Extract pricing information accurately.
    
    Context: You are analyzing a product page to identify pricing details.
    
    Using Reflexion:
    1. Initial Analysis:
       - Look for explicit price numbers
       - Identify pricing models (subscription, one-time, etc.)
       - Note any tiered pricing
    
    2. Verification:
       - Is this the current price?
       - Is it the base price or with add-ons?
       - Are there any conditions or caveats?
    
    3. Final Check:
       - Confirm the pricing is complete and accurate
    
    Content: {text}
    
    Return only the verified price information:""",
    
    'target_audience': """Task: Identify the intended target audience.
    
    Context: You are analyzing product marketing content to determine the ideal customer profile.
    
    Using Generate-Knowledge Prompting:
    1. Explicit Indicators:
       - Direct mentions of target users
       - Industry-specific terminology
       - Use cases described
    
    2. Implicit Signals:
       - Technical complexity level
       - Pricing structure implications
       - Feature sophistication
       - Language and tone used
    
    3. Synthesize:
       - Combine explicit and implicit indicators
       - Create a clear target audience profile
    
    Content: {text}
    
    Target audience:"""
} 