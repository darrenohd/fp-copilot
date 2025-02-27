"""
Test cases for RAG evaluation.
"""

RAG_TEST_CASES = [
    {
        "query": "What customer problem is the priority micro-adjust feature designed to solve?",
        "documents": [
            {
                "content": "A very common use case we encounter is global stack-ranking: customers want to form a stable, opinionated order of priority across all of their backlog items. Today, we provide a global manual ordering feature, which we recommend for these cases. There are several key issues with the current manual ordering system: Instability, Local vs. Global Sorting, Redundancy with Priority Field.",
                "expected_relevance": "relevant"
            },
            {
                "content": "Customer Messaging: Make fine-grained adjustments to priority levels within basic categories. If you implement a stack-ranking system for your tasks and projects, this is specifically made for you!",
                "expected_relevance": "unrelated"
            },
            {
                "content": "MS2 – Beta: Change management – Initialize using the manual sort index. When releasing this to actual users, we need to bootstrap their initial microadjust ordering.",
                "expected_relevance": "unrelated"
            }
        ]
    },
    {
        "query": "What solution is proposed to address the issues with the current manual ordering system?",
        "documents": [
            {
                "content": "We're simply going to allow users to adjust and rearrange the relative priority of their issues within a priority bucket, through drag-and-drop. Once we have this, we will strongly recommend to users that all stack-ranking use-cases be achieved through priority + micro-adjust.",
                "expected_relevance": "relevant"
            },
            {
                "content": "Options we considered but decided against: 1. Custom priority levels. Doesn't really solve for stack ranking, and would encourage stack-rankers to make way too many distinct categories. 2. Custom fields. Would solve for stack-ranking... but it's out of character for Linear.",
                "expected_relevance": "unrelated"
            },
            {
                "content": "Mockups & prototypes: Adjust issues within and between priorities …",
                "expected_relevance": "unrelated"
            }
        ]
    },
    {
        "query": "What alternatives were considered and ultimately rejected for handling stack ranking?",
        "documents": [
            {
                "content": "Options we considered but decided against: 1. Custom priority levels. Doesn't really solve for stack ranking, and would encourage stack-rankers to make way too many distinct categories. 2. Custom fields. Would solve for stack-ranking... but it's out of character for Linear.",
                "expected_relevance": "relevant"
            },
            {
                "content": "Prior art: We know of no other tool that offers manual adjustment within priorities; they all take one of the options we decided against…",
                "expected_relevance": "unrelated"
            },
            {
                "content": "We're simply going to allow users to adjust and rearrange the relative priority of their issues within a priority bucket, through drag-and-drop. Once we have this, we will strongly recommend to users that all stack-ranking use-cases be achieved through priority + micro-adjust.",
                "expected_relevance": "unrelated"
            }
        ]
    },
    {
        "query": "Does the PRD mention any prior art or competitor features related to manual priority adjustment?",
        "documents": [
            {
                "content": "Prior art: We know of no other tool that offers manual adjustment within priorities; they all take one of the options we decided against…",
                "expected_relevance": "relevant"
            },
            {
                "content": "Options we considered but decided against: 1. Custom priority levels. Doesn't really solve for stack ranking, and would encourage stack-rankers to make way too many distinct categories. 2. Custom fields. Would solve for stack-ranking... but it's out of character for Linear.",
                "expected_relevance": "unrelated"
            },
            {
                "content": "Resulting changelog: https://linear.app/changelog/2024-07-25-priority-for-projects-and-micro-adjust",
                "expected_relevance": "unrelated"
            }
        ]
    },
    {
        "query": "How are beta users expected to experience change management for the priority micro-adjust feature?",
        "documents": [
            {
                "content": "MS2 – Beta: Change management – Initialize using the manual sort index. When releasing this to actual users, we need to bootstrap their initial microadjust ordering.",
                "expected_relevance": "relevant"
            },
            {
                "content": "Customer Messaging: Make fine-grained adjustments to priority levels within basic categories. If you implement a stack-ranking system for your tasks and projects, this is specifically made for you!",
                "expected_relevance": "unrelated"
            },
            {
                "content": "Resulting changelog: https://linear.app/changelog/2024-07-25-priority-for-projects-and-micro-adjust",
                "expected_relevance": "unrelated"
            }
        ]
    },
    {
        "query": "What is the color scheme used in the mockups for the priority micro-adjust feature?",
        "documents": [
            {
                "content": "Mockups & prototypes: Adjust issues within and between priorities …",
                "expected_relevance": "unrelated"
            },
            {
                "content": "We're simply going to allow users to adjust and rearrange the relative priority of their issues within a priority bucket, through drag-and-drop. Once we have this, we will strongly recommend to users that all stack-ranking use-cases be achieved through priority + micro-adjust.",
                "expected_relevance": "unrelated"
            },
            {
                "content": "A very common use case we encounter is global stack-ranking: customers want to form a stable, opinionated order of priority across all of their backlog items. Today, we provide a global manual ordering feature, which we recommend for these cases.",
                "expected_relevance": "unrelated"
            }
        ]
    },
    {
        "query": "What release date can be inferred from the changelog URL in the PRD?",
        "documents": [
            {
                "content": "Resulting changelog: https://linear.app/changelog/2024-07-25-priority-for-projects-and-micro-adjust",
                "expected_relevance": "relevant"
            },
            {
                "content": "MS2 – Beta: Change management – Initialize using the manual sort index. When releasing this to actual users, we need to bootstrap their initial microadjust ordering.",
                "expected_relevance": "unrelated"
            },
            {
                "content": "Customer Messaging: Make fine-grained adjustments to priority levels within basic categories. If you implement a stack-ranking system for your tasks and projects, this is specifically made for you!",
                "expected_relevance": "unrelated"
            }
        ]
    },
    {
        "query": "What context is provided regarding customer messaging for the feature?",
        "documents": [
            {
                "content": "Customer Messaging: Make fine-grained adjustments to priority levels within basic categories. If you implement a stack-ranking system for your tasks and projects, this is specifically made for you!",
                "expected_relevance": "relevant"
            },
            {
                "content": "We're simply going to allow users to adjust and rearrange the relative priority of their issues within a priority bucket, through drag-and-drop. Once we have this, we will strongly recommend to users that all stack-ranking use-cases be achieved through priority + micro-adjust.",
                "expected_relevance": "unrelated"
            },
            {
                "content": "Prior art: We know of no other tool that offers manual adjustment within priorities; they all take one of the options we decided against…",
                "expected_relevance": "unrelated"
            }
        ]
    }
]

# ---------------------------------------------------------------------------
# RAG Evaluation Items based on the "Priority micro-adjust PRD"
# ---------------------------------------------------------------------------

# RAG Eval 1:
# [Question]: What customer problem is the priority micro-adjust feature designed to solve?
# [Reference text]: "A very common use case we encounter is global stack-ranking: customers want to form a stable, opinionated order of priority across all of their backlog items. Today, we provide a global manual ordering feature, which we recommend for these cases. There are several key issues with the current manual ordering system: Instability, Local vs. Global Sorting, Redundancy with Priority Field."
# Expected evaluation: relevant

# RAG Eval 2:
# [Question]: What solution is proposed to address the issues with the current manual ordering system?
# [Reference text]: "We're simply going to allow users to adjust and rearrange the relative priority of their issues within a priority bucket, through drag-and-drop. Once we have this, we will strongly recommend to users that all stack-ranking use-cases be achieved through priority + micro-adjust."
# Expected evaluation: relevant

# RAG Eval 3:
# [
