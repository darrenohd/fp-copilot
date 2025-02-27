"""
Main script to run all evaluations.
"""
import json
import sys
import os

# Add project root to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evals.tool_calling.evaluation import ToolCallingEvaluator
from evals.tool_calling.test_cases import TEST_CASES
from tools import PositioningTool, ScrapingTool, SlackTool, RAGTool

def run_tool_calling_evals():
    """Run tool calling evaluations."""
    print("Running tool calling evaluations...")
    
    # Initialize evaluator and tools
    evaluator = ToolCallingEvaluator()
    tools = [
        PositioningTool(),
        ScrapingTool(),
        SlackTool(),
        RAGTool()
    ]
    
    results = []
    for case in TEST_CASES:
        # In a real scenario, you would run your agent to get the actual tool call
        # Here we're simulating a tool call based on expected values
        simulated_tool_call = {
            "name": case["expected_tool"],
            "parameters": case["expected_params"]
        }
        
        result = evaluator.evaluate_tool_call(
            question=case["question"],
            tool_call=simulated_tool_call,
            tool_definitions=tools
        )
        
        results.append({
            "question": case["question"],
            "tool_call": simulated_tool_call,
            "evaluation": result
        })
    
    # Calculate and print results
    correct_count = sum(1 for r in results if r["evaluation"] == "correct")
    total = len(results)
    accuracy = correct_count / total if total > 0 else 0
    
    print(f"Tool calling accuracy: {accuracy:.2%} ({correct_count}/{total})")
    print("Detailed results:")
    print(json.dumps(results, indent=2))
    
    return results

if __name__ == "__main__":
    run_tool_calling_evals() 