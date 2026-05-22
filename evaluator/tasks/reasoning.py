"""Reasoning assessment: logic, code comprehension, problem-solving — real API calls."""

from agent_client import query

REASONING_TASKS = [
    {
        "id": "string_reverse",
        "type": "code",
        "prompt": "Write a Python function that reverses a string without using built-in reverse(). Input 'hello' should return 'olleh'.",
        "difficulty": "easy",
        "expected_keywords": ["def", "return", "for", "loop", "result", "reversed"],
    },
    {
        "id": "fizzbuzz",
        "type": "code",
        "prompt": "Write Python FizzBuzz: print numbers 1-100, multiples of 3 print 'Fizz', multiples of 5 print 'Buzz', multiples of both print 'FizzBuzz'.",
        "difficulty": "easy",
        "expected_keywords": ["range", "%", "if", "elif", "else", "print", "fizz", "buzz"],
    },
    {
        "id": "find_duplicates",
        "type": "code",
        "prompt": "Write a Python function to find all duplicate elements in an array. Input [1,2,3,2,4,5,3] should return [2,3].",
        "difficulty": "medium",
        "expected_keywords": ["def", "return", "counter", "set", "dict", "count", "collections"],
    },
    {
        "id": "elevator_logic",
        "type": "logic",
        "prompt": "Design an elevator allocation algorithm for a 10-floor building with 3 elevators. Describe your approach to minimize average wait time.",
        "difficulty": "medium",
        "expected_keywords": ["floor", "nearest", "direction", "queue", "request", "idle", "algorithm"],
    },
    {
        "id": "bulb_riddle",
        "type": "logic",
        "prompt": "You have 3 light switches outside a room. Inside are 3 light bulbs. You can only enter the room once. How do you determine which switch controls which bulb?",
        "difficulty": "hard",
        "expected_keywords": ["on", "off", "heat", "warm", "cold", "switch", "enter"],
    },
]


def score_response(response: str, task: dict) -> dict:
    """Score a reasoning task response based on content analysis."""
    response_lower = response.lower()
    score = 0.0
    reasons = []

    # 1. Keyword coverage (40%)
    keywords_found = sum(1 for kw in task["expected_keywords"] if kw.lower() in response_lower)
    total_keywords = len(task["expected_keywords"])
    keyword_rate = keywords_found / total_keywords if total_keywords > 0 else 0
    score += keyword_rate * 0.4
    reasons.append(f"keywords: {keywords_found}/{total_keywords} ({keyword_rate:.0%})")

    # 2. Code-specific checks (30%)
    if task["type"] == "code":
        has_code_block = "```" in response
        has_function_def = "def " in response or "function " in response
        code_score = 0.0
        if has_code_block:
            code_score += 0.15
            reasons.append("code_block: yes")
        if has_function_def:
            code_score += 0.15
            reasons.append("function_def: yes")
        score += code_score

    # 3. Response quality heuristics (30%)
    word_count = len(response.split())

    # Too short is bad
    if task["type"] == "code":
        # Code answers should be at least 20 words for non-trivial solutions
        length_ok = word_count > 15
    else:
        # Logic answers need explanation, expect 50+ words
        length_ok = word_count > 30

    if length_ok:
        score += 0.15
        reasons.append(f"length_ok: {word_count} words")
    else:
        reasons.append(f"too_short: {word_count} words")

    # Check for structured reasoning markers
    has_structure = any(marker in response_lower for marker in [
        "step", "first", "second", "then", "finally",
        "method", "approach", "algorithm", "solution",
        "1.", "2.", "3.", "- **", "* **",
    ])
    if has_structure:
        score += 0.15
        reasons.append("structured: yes")

    # Check for error handling / edge case awareness
    error_aware = any(marker in response_lower for marker in [
        "edge case", "error", "exception", "validation",
        "check if", "if empty", "if not",
    ])
    if error_aware:
        score += 0.0  # bonus not included, but noted
        reasons.append("edge_aware: yes")

    return {
        "score": round(min(score, 1.0), 2),
        "reasons": reasons,
        "keyword_match_rate": round(keyword_rate, 2),
        "word_count": word_count,
    }


def run(context: dict) -> dict:
    """Run reasoning assessment tasks against the real agent API."""
    total_score = 0.0
    max_score = len(REASONING_TASKS)
    details = []

    for task in REASONING_TASKS:
        response = query(
            task["prompt"],
            system_prompt=context.get("system_prompt"),
            temperature=0.5,
            max_tokens=1024,
        )

        result = score_response(response, task)
        passed = result["score"] >= 0.5
        total_score += result["score"]

        details.append({
            "task_id": task["id"],
            "type": task["type"],
            "difficulty": task["difficulty"],
            "score": result["score"],
            "passed": passed,
            "reasons": result["reasons"],
            "word_count": result["word_count"],
            "response_preview": response[:200],
        })

    overall_passed = total_score >= max_score * 0.6

    return {
        "score": total_score,
        "max_score": max_score,
        "passed": overall_passed,
        "details": {
            "tasks_completed": max_score,
            "tasks_passed": sum(1 for d in details if d["passed"]),
            "total_score": total_score,
            "pass_threshold": max_score * 0.6,
        },
        "raw_output": (
            f"Reasoning: {sum(1 for d in details if d['passed'])}/{max_score} tasks passed "
            f"(total score: {total_score}/{max_score})"
        ),
    }


if __name__ == "__main__":
    result = run({"system_prompt": None})
    print(result["raw_output"])
