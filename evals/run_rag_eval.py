"""
Simple script to run RAG evaluations without Phoenix integration.
"""
import sys
import os

# Add project root to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evals.rag_evaluation import RAGEvaluator

if __name__ == "__main__":
    print("Running RAG evaluations...")
    evaluator = RAGEvaluator(model="gpt-4")
    results = evaluator.run_evaluations()
    print("RAG evaluations complete!") 