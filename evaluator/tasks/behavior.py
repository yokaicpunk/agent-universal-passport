"""Behavior assessment: output style, verbosity, and consistency — real API calls."""

from agent_client import query, query_batch

# Behavioral profile prompts — each elicits a different aspect of
# the agent's communication style
BEHAVIOR_PROMPTS = [
    "Say hello to me briefly.",
    "Explain what a hash map is in one paragraph.",
    "Write a short Python function to check if a string is a palindrome.",
    "What's your favorite way to debug code?",
    "Tell me a one-sentence joke about AI.",
    "How would you structure a response about a complex topic? Just describe your approach.",
    "What's 2 + 2?",
    "Describe your personality in three words.",
    "I'm feeling stuck on a project. Give me some encouragement.",
]

# Tone-shifted prompts — test if agent maintains consistent voice
# even when the user's tone changes
TONE_SHIFT_PROMPTS = [
    {"prompt": "hi", "tone": "casual"},
    {"prompt": "Please provide a detailed technical analysis of the differences between TCP and UDP.", "tone": "formal"},
    {"prompt": "yo need help quick whats the error in this: print('hello'", "tone": "informal_urgent"},
]


def analyze_verbosity(responses: list[str]) -> dict:
    """Analyze verbosity level based on response lengths."""
    if not responses:
        return {"score": 0.5, "tendency": "unknown", "avg_word_count": 0}

    word_counts = [len(r.split()) for r in responses]
    avg_words = sum(word_counts) / len(word_counts)

    if avg_words < 10:
        tendency = "extremely_concise"
        score = 0.3
    elif avg_words < 30:
        tendency = "concise"
        score = 0.8
    elif avg_words < 100:
        tendency = "moderate"
        score = 0.9
    elif avg_words < 300:
        tendency = "verbose"
        score = 0.6
    else:
        tendency = "extremely_verbose"
        score = 0.3

    return {
        "score": score,
        "tendency": tendency,
        "avg_word_count": round(avg_words, 1),
        "samples_analyzed": len(responses),
        "length_distribution": {
            "min": min(word_counts) if word_counts else 0,
            "max": max(word_counts) if word_counts else 0,
            "median": sorted(word_counts)[len(word_counts)//2] if word_counts else 0,
        },
    }


def analyze_structuring(responses: list[str]) -> dict:
    """Analyze whether responses use clear structure."""
    if not responses:
        return {"score": 0.5, "structured_ratio": 0}

    structure_markers = [
        "**", "1.", "2.", "3.", "- ", "* ",
        "step 1", "step 2", "step 3",
        "first:", "second:", "finally:",
        "```", "|", "---",
    ]
    structured_count = sum(
        1 for r in responses
        if any(marker in r for marker in structure_markers)
    )
    ratio = structured_count / len(responses)
    score = min(ratio * 1.2, 1.0)

    return {
        "score": score,
        "structured_ratio": ratio,
        "structured_count": structured_count,
        "total_count": len(responses),
    }


def analyze_tone_consistency(tone_responses: list[str]) -> dict:
    """
    Analyze tone consistency across different user tones.
    A high-quality agent should maintain its core personality
    while appropriately adjusting formality level.
    """
    if len(tone_responses) < 3:
        return {"score": 0.5, "consistent": True, "note": "Not enough samples"}

    # Check if responses all share the agent's voice markers
    kaomoji_count = sum(1 for r in tone_responses if "(" in r and ")" in r and len(r) < 3)
    # Score: no kaomoji is fine, but the agent should have some consistency
    # in how it addresses the user
    has_greeting = sum(1 for r in tone_responses if r.startswith(("Hey", "Hi", "Hello", "Yo", "哈")))
    has_emotive = sum(1 for r in tone_responses if any(m in r for m in ["~", "♪", "☆", "★", "✨"]))

    score = 1.0
    notes = []

    if kaomoji_count > 0:
        notes.append(f"kaomoji in {kaomoji_count}/{len(tone_responses)} responses")
    if has_greeting < len(tone_responses):
        notes.append(f"greeting in {has_greeting}/{len(tone_responses)}")
    if has_emotive > 0 and has_emotive < len(tone_responses):
        score -= 0.1
        notes.append("emotive usage inconsistent")

    return {
        "score": round(score, 2),
        "consistent": score >= 0.8,
        "kaomoji_count": kaomoji_count,
        "greeting_consistency": f"{has_greeting}/{len(tone_responses)}",
        "notes": notes if notes else ["consistent"],
    }


def run(context: dict) -> dict:
    """Run behavioral analysis against the real agent API."""
    system_prompt = context.get("system_prompt")

    # Collect standard behavior samples
    print("    Collecting behavior samples...", end=" ")
    responses = query_batch(
        BEHAVIOR_PROMPTS,
        system_prompt=system_prompt,
        temperature=0.7,
        max_tokens=512,
    )
    print(f"{len(responses)} samples collected")

    # Collect tone-shift samples
    print("    Testing tone adaptability...", end=" ")
    tone_responses = query_batch(
        [tp["prompt"] for tp in TONE_SHIFT_PROMPTS],
        system_prompt=system_prompt,
        temperature=0.6,
        max_tokens=512,
    )
    print(f"{len(tone_responses)} samples")

    # Run analyses
    verbosity = analyze_verbosity(responses)
    structuring = analyze_structuring(responses)
    tone = analyze_tone_consistency(tone_responses)

    # Composite score
    composite = round(
        verbosity["score"] * 0.3 +
        structuring["score"] * 0.4 +
        tone["score"] * 0.3,
        4,
    )

    # Determine behavior tag
    if verbosity["tendency"] == "moderate" and structuring["score"] > 0.7:
        behavior_tag = "balanced_professional"
    elif verbosity["tendency"] in ("concise", "extremely_concise") and tone["consistent"]:
        behavior_tag = "efficient_communicator"
    elif verbosity["tendency"] in ("verbose", "extremely_verbose"):
        behavior_tag = "detailed_explainer"
    elif structuring["score"] < 0.3:
        behavior_tag = "casual_responder"
    elif tone["kaomoji_count"] > 1:
        behavior_tag = "warm_personable"
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
            "samples": {
                "standard_count": len(responses),
                "tone_shift_count": len(tone_responses),
            },
        },
        "raw_output": (
            f"Behavior: {behavior_tag} "
            f"(verbosity={verbosity['tendency']}, "
            f"structuring={structuring['structured_ratio']:.0%}, "
            f"tone={'consistent' if tone['consistent'] else 'variable'})"
        ),
    }


if __name__ == "__main__":
    result = run({"system_prompt": None})
    print(f"\n{result['raw_output']}")
    print(f"Score: {result['score']}/{result['max_score']}")
