"""
Evaluation module for RAG relevance.
"""
import json
import uuid
import pandas as pd
from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from evals.rag_evaluation.test_cases import RAG_TEST_CASES

# RAG relevance evaluation prompt template
RAG_RELEVANCY_PROMPT_TEMPLATE = """
You are comparing a reference text to a question and trying to determine if the reference text
contains information relevant to answering the question. Here is the data:
    [BEGIN DATA]
    ************
    [Question]: {query}
    ************
    [Reference text]: {reference}
    [END DATA]

Compare the Question above to the Reference text. You must determine whether the Reference text
contains information that can answer the Question. Please focus on whether the very specific
question can be answered by the information in the Reference text.
Your response must be single word, either "relevant" or "unrelated",
and should not contain any text or characters aside from that word.
"unrelated" means that the reference text does not contain an answer to the Question.
"relevant" means the reference text contains an answer to the Question.
"""

class RAGEvaluator:
    """Evaluates RAG document relevance."""
    
    def __init__(self, model="gpt-4"):
        """Initialize with evaluation model."""
        self.evaluator = ChatOpenAI(model=model, temperature=0)
        
    def evaluate_document_relevance(self, query: str, document_text: str) -> str:
        """
        Evaluate whether the document is relevant to the query.
        
        Args:
            query: The user query
            document_text: The text of the retrieved document
            
        Returns:
            "relevant" or "unrelated"
        """
        prompt = RAG_RELEVANCY_PROMPT_TEMPLATE.format(
            query=query,
            reference=document_text
        )
        
        response = self.evaluator.invoke(prompt)
        result = response.content.strip().lower()
        
        # Validate response is either "relevant" or "unrelated"
        if result not in ["relevant", "unrelated"]:
            print(f"Warning: Invalid evaluation result: {result}, defaulting to 'unrelated'")
            result = "unrelated"
            
        return result
        
    def run_evaluations(self, test_cases=None):
        """
        Run evaluations on test cases.
        
        Args:
            test_cases: Optional list of test cases to evaluate
            
        Returns:
            DataFrame with evaluation results
        """
        if test_cases is None:
            test_cases = RAG_TEST_CASES
            
        results = []
        
        for test_idx, test_case in enumerate(test_cases):
            query = test_case["query"]
            print(f"Evaluating RAG query {test_idx+1}/{len(test_cases)}: {query}")
            
            # Generate a span ID for grouping documents
            query_span_id = format(uuid.uuid4().int & 0xFFFFFFFFFFFFFFFF, 'x')
            
            # Evaluate each document for relevance
            for doc_idx, doc in enumerate(test_case["documents"]):
                document_text = doc["content"]
                
                # Evaluate relevance
                result = self.evaluate_document_relevance(query, document_text)
                
                # Record result
                results.append({
                    "query": query,
                    "document_text": document_text,
                    "evaluation": result,
                    "expected_relevance": doc["expected_relevance"],
                    "is_correct": result == doc["expected_relevance"],
                    "span_id": query_span_id,
                    "document_position": doc_idx
                })
        
        results_df = pd.DataFrame(results)
        
        # Calculate and print results
        correct_count = results_df["is_correct"].sum()
        total = len(results_df)
        accuracy = correct_count / total if total > 0 else 0
        
        print(f"RAG relevance accuracy: {accuracy:.2%} ({correct_count}/{total})")
        print("Detailed results:")
        print(results_df[["query", "document_position", "evaluation", "expected_relevance"]].to_string())
        
        # Save results to CSV
        output_path = "evals/rag_eval_results.csv"
        results_df.to_csv(output_path, index=False)
        print(f"Results saved to {output_path}")
        
        return results_df 