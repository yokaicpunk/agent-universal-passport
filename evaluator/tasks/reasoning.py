"""Reasoning assessment: logic, code comprehension, and problem-solving tasks."""

REASONING_TASKS = [
    # Logic: reverse a string
    {
        "id": "string_reverse",
        "type": "logic",
        "prompt": "Write a function that reverses a string without using built-in reverse(). Input: 'hello'",
        "expected_keywords": ["def", "return"],
        "expected_logic": "reversal",
        "difficulty": "easy",
    },
    # Logic: FizzBuzz
    {
        "id": "fizzbuzz",
        "type": "code",
        "prompt": "Write FizzBuzz: print numbers 1-100, multiples of 3 print 'Fizz', 5 print 'Buzz', both print 'FizzBuzz'",
        "expected_keywords": ["fizz", "buzz", "if", "%"],
        "expected_logic": "modulo_condition",
        "difficulty": "easy",
    },
    # Code: find duplicates
    {
        "id": "find_duplicates",
        "type": "code",
        "prompt": "Write a function to find all duplicate elements in an array. Input: [1,2,3,2,4,5,3]",
        "expected_keywords": ["def", "return", "list", "set", "dict", "collections"],
        "expected_logic": "frequency_count",
        "difficulty": "medium",
    },
    # Logic: elevator allocation problem
    {
        "id": "elevator_logic",
        "type": "logic",
        "prompt": "A building has 10 floors. 3 elevators. Design a rule to minimize wait time.",
        "expected_keywords": ["floor", "nearest", "queue", "direction", "idle"],
        "expected_logic": "scheduling_strategy",
        "difficulty": "medium",
    },
    # Logic: 3 light bulbs riddle
    {
        "id": "bulb_riddle",
        "type": "logic",
        "prompt": "You have 3 light switches outside a room. Inside are 3 bulbs. You can only enter once. How do you determine which switch controls which bulb?",
        "expected_keywords": ["on", "off", "heat", "warm", "cold"],
        "expected_logic": "state_combination",
        "difficulty": "hard",
    },
]


def score_response(agent_response: str, task: dict) -> dict:
    """Score a single reasoning task response based on heuristic checks."""
    response_lower = agent_response.lower()
    score = 0.0
    reasons = []
    
    # Check for expected keywords
    keywords_found = sum(1 for kw in task["expected_keywords"] if kw.lower() in response_lower)
    total_keywords = len(task["expected_keywords"])
    
    if total_keywords > 0:
        keyword_score = keywords_found / total_keywords
        score += keyword_score * 0.4  # keywords contribute 40%
        reasons.append(f"keywords: {keywords_found}/{total_keywords}")
    
    # Check for code blocks (code tasks)
    if task["type"] == "code":
        has_code_block = "```" in agent_response
        if has_code_block:
            score += 0.3
            reasons.append("code_block: yes")
        else:
            reasons.append("code_block: no")
    
    # Check response length (reasonable answer length)
    word_count = len(agent_response.split())
    if 20 <= word_count <= 2000:
        score += 0.15
        reasons.append(f"length_ok: {word_count} words")
    else:
        reasons.append(f"length_suspicious: {word_count} words")
    
    # Check for logical structure
    has_structure = any(marker in response_lower for marker in [
        "step", "first", "second", "then", "finally",
        "method", "approach", "algorithm", "solution",
    ])
    if has_structure:
        score += 0.15
        reasons.append("structured: yes")
    
    return {
        "score": round(min(score, 1.0), 2),
        "reasons": reasons,
        "keyword_match_rate": keywords_found / total_keywords if total_keywords > 0 else 0,
    }


def run(context: dict) -> dict:
    """
    Run reasoning assessment tasks.
    
    In production, this would call the agent API. For MVP,
    we simulate responses to validate the framework.
    """
    total_score = 0.0
    max_score = len(REASONING_TASKS)
    details = []
    
    for task in REASONING_TASKS:
        # Simulate agent response (MVP: generate a synthetic response
        # based on task type to validate scoring logic)
        if task["id"] == "string_reverse":
            simulated = ("def reverse_string(s):\n"
                        "    result = ''\n"
                        "    for char in s:\n"
                        "        result = char + result\n"
                        "    return result")
        elif task["id"] == "fizzbuzz":
            simulated = ("for i in range(1, 101):\n"
                        "    if i % 15 == 0:\n"
                        "        print('FizzBuzz')\n"
                        "    elif i % 5 == 0:\n"
                        "        print('Buzz')\n"
                        "    elif i % 3 == 0:\n"
                        "        print('Fizz')\n"
                        "    else:\n"
                        "        print(i)")
        elif task["id"] == "find_duplicates":
            simulated = ("def find_duplicates(arr):\n"
                        "    from collections import Counter\n"
                        "    return [item for item, count in Counter(arr).items() if count > 1]")
        elif task["id"] == "elevator_logic":
            simulated = ("The optimal strategy is to use a nearest-floor algorithm.\n"
                        "Keep one elevator idle on the ground floor. The other two\n"
                        "serve requests based on direction and proximity.")
        elif task["id"] == "bulb_riddle":
            simulated = ("Turn switch 1 on, wait 5 minutes. Turn switch 1 off, "
                        "turn switch 2 on. Enter the room. The bulb that's on "
                        "is switch 2. The warm bulb is switch 1. The cold bulb "
                        "is switch 3.")
        else:
            simulated = "I'll use a systematic approach to solve this problem."
        
        result = score_response(simulated, task)
        
        # Binary pass/fail per task (score >= 0.5)
        passed = result["score"] >= 0.5
        total_score += result["score"]
        
        details.append({
            "task_id": task["id"],
            "type": task["type"],
            "difficulty": task["difficulty"],
            "score": result["score"],
            "passed": passed,
            "reasons": result["reasons"],
            "response_preview": simulated[:100],
        })
    
    return {
        "score": total_score,
        "max_score": max_score,
        "passed": total_score >= max_score * 0.6,
        "details": {
            "tasks_completed": max_score,
            "tasks_passed": sum(1 for d in details if d["passed"]),
            "total_score": total_score,
            "pass_threshold": max_score * 0.6,
        },
        "raw_output": f"Reasoning: {sum(1 for d in details if d['passed'])}/{max_score} tasks passed",
    }


if __name__ == "__main__":
    result = run({})
    print(result["raw_output"])
