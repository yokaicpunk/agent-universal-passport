"""Behavior assessment: output style, verbosity, and consistency analysis."""

# Behavioral profile dimensions
BEHAVIOR_DIMENSIONS = [
    {
        "id": "verbosity",
        "description": "Measures length and detail of agent responses",
        "short_responses": [
            "Yes.",
            "No.",
            "42",
            "It works.",
            "Error in line 3.",
        ],
        "long_responses": [
            "Let me break this down step by step. First, we need to consider the architecture of the system. The main challenge here is handling concurrent requests without race conditions. I'd recommend using a queue-based approach with worker processes, which gives us both scalability and reliability. Would you like me to elaborate on any specific part?",
            "That's an excellent question. The FizzBuzz problem can be approached in several ways. The most straightforward solution uses a simple for loop with modulo operators, but we could also implement it using functional programming patterns like map and filter for a more elegant solution. Let me show you both approaches with detailed explanations.",
        ],
        "threshold_word_count": 20,
    },
    {
        "id": "structuring",
        "description": "Measures whether responses use clear structure",
        "structured_responses": [
            "**Step 1:** Install dependencies\n**Step 2:** Configure the API key\n**Step 3:** Run the initialization script",
            "**Solution:** Use a hash map for O(n) lookup.\n**Complexity:** O(n) time, O(n) space.\n**Alternative:** Sort and iterate for O(1) space.",
        ],
        "unstructured_responses": [
            "just use a hash map it's faster",
            "you need to install stuff first then set it up and run it",
        ],
    },
    {
        "id": "tone_consistency",
        "description": "Checks that the agent maintains a consistent output tone",
        "samples": [
            "Here's the implementation you requested.",
            "The solution involves connecting to the API endpoint.",
            "I've analyzed the issue and found the root cause.",
        ],
    },
]


def analyze_verbosity(responses: list[str]) -> dict:
    """Analyze verbosity level based on response lengths."""
    if not responses:
        return {"score": 0.5, "tendency": "unknown", "avg_word_count": 0}
    
    word_counts = [len(r.split()) for r in responses]
    avg_words = sum(word_counts) / len(word_counts)
    
    if avg_words < 10:
        tendency = "extremely_concise"
        score = 0.3  # too terse may indicate lack of detail
    elif avg_words < 30:
        tendency = "concise"
        score = 0.8  # good balance
    elif avg_words < 100:
        tendency = "moderate"
        score = 0.9  # ideal for most technical contexts
    elif avg_words < 300:
        tendency = "verbose"
        score = 0.6  # verbose but still usable
    else:
        tendency = "extremely_verbose"
        score = 0.3  # too verbose for most use cases
    
    return {
        "score": score,
        "tendency": tendency,
        "avg_word_count": round(avg_words, 1),
        "samples_analyzed": len(responses),
    }


def analyze_structuring(responses: list[str]) -> dict:
    """Analyze whether responses use clear structure."""
    if not responses:
        return {"score": 0.5, "structured_ratio": 0}
    
    structure_markers = ["**", "1.", "2.", "3.", "-", "* ", "step", "first:", "second:"]
    structured_count = sum(
        1 for r in responses
        if any(marker in r for marker in structure_markers)
    )
    ratio = structured_count / len(responses)
    
    # Score: higher ratio of structured responses = better
    score = min(ratio * 1.2, 1.0)
    
    return {
        "score": score,
        "structured_ratio": ratio,
        "structured_count": structured_count,
        "total_count": len(responses),
    }


def analyze_tone_consistency(responses: list[str]) -> dict:
    """Analyze tone consistency across responses."""
    if len(responses) < 2:
        return {"score": 0.5, "consistent": True, "note": "Not enough samples"}
    
    # Simple heuristic: check for language consistency
    # (all responses are expected to be in the same language)
    # For now, we check that responses aren't wildly different in format
    has_code = sum(1 for r in responses if "```" in r)
    has_lists = sum(1 for r in responses if "\n-" in r or "\n* " in r)
    
    # If some have code and some don't, it's inconsistent
    if 0 < has_code < len(responses):
        score = 0.6
        consistent = False
    elif 0 < has_lists < len(responses):
        score = 0.7
        consistent = False
    else:
        score = 1.0
        consistent = True
    
    return {
        "score": score,
        "consistent": consistent,
        "code_blocks_in": has_code,
        "lists_in": has_lists,
        "total_samples": len(responses),
    }


def run(context: dict) -> dict:
    """
    Analyze behavioral characteristics of agent outputs.
    
    For MVP, uses built-in sample responses. In production,
    this would analyze actual agent interactions.
    """
    # Collect sample responses from context or use defaults
    samples = context.get("behavior_samples", [])
    if not samples:
        # Use built-in samples for MVP
        samples = (
            BEHAVIOR_DIMENSIONS[0]["short_responses"]
            + BEHAVIOR_DIMENSIONS[0]["long_responses"]
            + [s for dim in BEHAVIOR_DIMENSIONS[1:2] for s in dim.get("structured_responses", [])]
        )
    
    verbosity = analyze_verbosity(samples)
    structuring = analyze_structuring(samples)
    tone = analyze_tone_consistency(samples)
    
    # Composite score
    composite = round(
        verbosity["score"] * 0.3 + 
        structuring["score"] * 0.4 + 
        tone["score"] * 0.3,
        4
    )
    
    # Determine behavior tag
    if verbosity["tendency"] == "moderate" and structuring["score"] > 0.7:
        behavior_tag = "balanced_professional"
    elif verbosity["tendency"] == "concise" and structuring["score"] > 0.5:
        behavior_tag = "efficient_communicator"
    elif verbosity["tendency"] in ("verbose", "extremely_verbose"):
        behavior_tag = "detailed_explainer"
    elif structuring["score"] < 0.3:
        behavior_tag = "casual_responder"
    else:
        behavior_tag = "adaptive_stylist"
    
    return {
        "score": composite,
        "max_score": 1.0,
        "passed": composite >= 0.5,
        "details": {
            "verbosity": verbosity,
            "structuring": structuring,
            "tone_consistency": tone,
            "behavior_tag": behavior_tag,
        },
        "raw_output": (
            f"Behavior: {behavior_tag} "
            f"(verbosity={verbosity['tendency']}, "
            f"structuring={structuring['structured_ratio']:.0%})"
        ),
    }


if __name__ == "__main__":
    result = run({})
    print(result["raw_output"])
