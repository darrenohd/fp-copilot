from langchain_openai import ChatOpenAI
import streamlit as st

class PositioningGenerator:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)
        
    def generate_positioning(self):
        # Gather all relevant information from vector store
        product_info = self._get_product_info()
        user_insights = self._get_user_insights()
        competitor_info = self._get_competitor_info()
        
        # Get feature info from session state
        feature_info = st.session_state.get('feature_info', {
            'name': 'Unnamed Feature',
            'release_date': 'TBD'
        })
        
        prompt = self._create_positioning_prompt(
            product_info, 
            user_insights, 
            competitor_info,
            feature_info
        )
        
        return self.llm.invoke(prompt).content
        
    def _get_product_info(self):
        return self.vector_store.similarity_search(
            "What are our product's key features and benefits?",
            filter={"doc_type": "requirements"}
        )
        
    def _get_user_insights(self):
        return self.vector_store.similarity_search(
            "What are the main user pain points and needs?",
            filter={"doc_type": "interviews"}
        )
        
    def _get_competitor_info(self):
        return self.vector_store.similarity_search(
            "What are competitor strengths and weaknesses?",
            filter={"type": "product_page"}
        )
        
    def _create_positioning_prompt(self, product_info, user_insights, competitor_info, feature_info):
        return f"""You are a senior product marketing strategist with expertise in market positioning and competitive analysis.

Task: Create a comprehensive product positioning analysis for {feature_info['name']}.

Feature Context:
- Feature Name: {feature_info['name']}
- Target Release: {feature_info['release_date']}

Step 1: Analyze the provided information systematically:
Product Information:
{self._format_docs(product_info)}

User Research:
{self._format_docs(user_insights)}

Competitive Landscape:
{self._format_docs(competitor_info)}

Step 2: Let's think through this step-by-step:
1. First, identify the key user pain points and needs
2. Then, map our product's features to these pain points
3. Next, analyze how competitors address these needs
4. Finally, identify our unique value proposition

Step 3: Based on this analysis, please provide:

1. Positioning Statement using this framework:
   For [target customer]
   Who [statement of need or opportunity]
   Our [product name]
   Is a [product category]
   That [key benefit/compelling reason to buy]
   Unlike [primary competitive alternative]
   Our product [key point of differentiation]

2. Top 3 User Pain Points (prioritized by severity and frequency)

3. Key Product Strengths (with evidence from requirements)

4. Areas for Improvement (based on competitive analysis)

5. Competitive Advantages (with specific differentiators)

Remember to:
- Be specific and evidence-based
- Focus on unique value propositions
- Use clear, measurable statements
- Maintain consistency across all points

Output Format: Use markdown formatting for clarity and structure.
"""

    def _format_docs(self, docs):
        return "\n".join([doc.page_content for doc in docs]) 