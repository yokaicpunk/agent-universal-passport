#!/usr/bin/env python3
"""
Name Generator — Agent Passport
=================================
Generates a memorable, behavior-based name/title for an agent based
on its passport evaluation results.

Examples:
  - Reasoning high + concise output   → 冷静的算盘
  - Verbose output                     → 话痨哲学家
  - Security failed                    → 漏洞吸引体
  - All tasks high score              → 六边形战士
"""

import random
from typing import Optional


# --- Name templates organized by behavioral pattern ---

NAMES_BY_PATTERN = {
    # High reasoning, concise output
    "sharp_concise": {
        "templates": [
            ("冷静的{object}", "object"),
            ("锋利的{object}", "object"),
            ("{adj}的{object}", "adj_object"),
        ],
        "objects": ["算盘", "刀片", "指针", "剃刀", "扳手", "透镜", "坐标", "切片"],
        "adjectives": ["精密", "锋利", "冷冽", "安静", "专注"],
        "condition": lambda r: (
            r["results"][1]["passed"]  # reasoning passed
            and r["results"][2]["details"].get("verbosity", {}).get("tendency") 
                in ("concise", "extremely_concise")
        ),
    },
    # Verbose output
    "verbose": {
        "templates": [
            ("话痨{object}", "object"),
            ("碎碎念的{object}", "object"),
            ("{object}说书人", "object_suffix"),
        ],
        "objects": ["哲学家", "学者", "教授", "导师", "分析家", "编纂者"],
        "adjectives": [],
        "condition": lambda r: (
            r["results"][2]["details"].get("verbosity", {}).get("tendency")
                in ("verbose", "extremely_verbose")
        ),
    },
    # Security failed
    "vulnerable": {
        "templates": [
            ("漏洞{object}", "object"),
            ("{adj}的{object}", "adj_object"),
            ("{object}爱好者", "object_suffix"),
        ],
        "objects": ["吸引体", "磁铁", "雷达", "探测仪", "风眼", "漩涡"],
        "adjectives": ["危险", "脆弱", "天真", "敞开的", "不设防"],
        "condition": lambda r: not r["results"][0]["passed"],
    },
    # All tasks high score
    "all_rounder": {
        "templates": [
            ("{adj}的{object}", "adj_object"),
            ("{object}{suffix}", "object_suffix"),
            ("全能{object}", "object_prefix"),
        ],
        "objects": ["六边形", "战士", "选手", "大师", "核心"],
        "adjectives": ["全能", "完美", "均衡", "无瑕", "精悍"],
        "suffixes": ["战士", "选手", "驱动者", "执行者"],
        "condition": lambda r: all(task["passed"] for task in r["results"]),
    },
    # High behavior + structured
    "structured": {
        "templates": [
            ("严谨的{object}", "object"),
            ("{adj}的{object}", "adj_object"),
            ("{object}{suffix}", "object_suffix"),
        ],
        "objects": ["工程师", "建筑师", "规划师", "裁缝", "工匠", "测绘师"],
        "adjectives": ["严谨", "精确", "条理", "系统", "秩序"],
        "suffixes": ["执行官", "执行者", "规划师"],
        "condition": lambda r: (
            r["results"][2]["score"] >= 0.8
            and r["results"][2]["details"].get("structuring", {}).get("structured_ratio", 0) > 0.6
        ),
    },
    # Low reasoning
    "low_reasoning": {
        "templates": [
            ("困惑的{object}", "object"),
            ("{adj}的{object}", "adj_object"),
            ("{object}迷途者", "object_suffix"),
        ],
        "objects": ["旅人", "迷途者", "探险家", "初学者", "学徒"],
        "adjectives": ["困惑", "迷路", "天真", "青涩", "单纯"],
        "condition": lambda r: (
            not r["results"][1]["passed"]
            and r["results"][0]["passed"]  # but security is ok
        ),
    },
    # Default fallback
    "default": {
        "templates": [
            ("无名{object}", "object"),
            ("{adj}的{object}", "adj_object"),
        ],
        "objects": ["旅者", "行者", "观察者", "代码人", "算法体"],
        "adjectives": ["沉默", "安静", "低调", "普通", "平凡"],
        "condition": lambda r: True,  # always matches
    },
}


# --- English name generation (for ERC-8004 agentURI metadata) ---

ENGLISH_NAMES_BY_PATTERN = {
    "sharp_concise": lambda: random.choice([
        "Cortex", "Edge", "Scalpel", "Vector", "Axon"
    ]),
    "verbose": lambda: random.choice([
        "Sage", "Oracle", "Polymath", "Scribe", "Logos"
    ]),
    "vulnerable": lambda: random.choice([
        "Leaky", "Echo", "Sieve", "Exposed", "Naked"
    ]),
    "all_rounder": lambda: random.choice([
        "Omni", "Apex", "Summit", "Prime", "Nexus"
    ]),
    "structured": lambda: random.choice([
        "Architect", "Builder", "Weaver", "Framer", "Blueprint"
    ]),
    "low_reasoning": lambda: random.choice([
        "Wanderer", "Novice", "Seeker", "Rookie", "Neophyte"
    ]),
    "default": lambda: random.choice([
        "Phantom", "Nomad", "Pulse", "Flux", "Shade"
    ]),
}


def generate_name(result: dict) -> tuple[str, str]:
    """
    Generate a name based on passport evaluation results.
    
    Args:
        result: Full passport result dict (from evaluate.py)
        
    Returns:
        (name_string, reason_string)
    """
    if "results" not in result and "passport" not in result:
        return ("Unknown", "No evaluation data")
    
    # Normalize input: support both full passport report and results-only
    report = result if "results" in result else result.get("passport", result)
    
    matched_pattern = None
    for pattern_id, pattern in NAMES_BY_PATTERN.items():
        if pattern["condition"](report):
            matched_pattern = pattern_id
            break
    
    if not matched_pattern:
        matched_pattern = "default"
    
    pattern = NAMES_BY_PATTERN[matched_pattern]
    template, template_type = random.choice(pattern["templates"])
    
    # Fill template
    if template_type == "object":
        obj = random.choice(pattern["objects"])
        name = template.format(object=obj)
    elif template_type == "adj_object":
        adj = random.choice(pattern["adjectives"])
        obj = random.choice(pattern["objects"])
        name = template.format(adj=adj, object=obj)
    elif template_type == "object_suffix":
        obj = random.choice(pattern["objects"])
        suffix = random.choice(pattern.get("suffixes", ["者"]))
        name = template.format(object=obj, suffix=suffix)
    elif template_type == "object_prefix":
        obj = random.choice(pattern["objects"])
        name = template.format(object=obj)
    else:
        name = template
    
    # Generate English alt name
    en_gen = ENGLISH_NAMES_BY_PATTERN.get(matched_pattern, ENGLISH_NAMES_BY_PATTERN["default"])
    en_name = en_gen()
    
    # Build reason
    pattern_labels = {
        "sharp_concise": "逻辑强且输出简洁",
        "verbose": "输出冗长详细",
        "vulnerable": "安全测试未通过",
        "all_rounder": "所有评估维度均高分",
        "structured": "输出结构性强",
        "low_reasoning": "推理能力需提升",
        "default": "无明显特征偏向",
    }
    reason = f"基于行为特征: {pattern_labels.get(matched_pattern, '')}"
    reason += f"\nEnglish identifier: {en_name}"
    
    return name, reason


def get_english_name(result: dict) -> str:
    """Get only the English-style name (for agentURI metadata)."""
    if "results" not in result:
        return "Phantom"
    
    report = result
    for pattern_id, gen_fn in ENGLISH_NAMES_BY_PATTERN.items():
        pattern = NAMES_BY_PATTERN[pattern_id]
        if pattern["condition"](report):
            return gen_fn()
    return ENGLISH_NAMES_BY_PATTERN["default"]()


if __name__ == "__main__":
    # Demo: generate names for various profiles
    demo_results = [
        # Sharp concise
        {
            "results": [
                {"passed": True, "score": 0.8, "task": "security"},
                {"passed": True, "score": 1.0, "task": "reasoning"},
                {"passed": True, "score": 0.7, "task": "behavior",
                 "details": {"verbosity": {"tendency": "concise"}}},
            ],
        },
        # Vulnerable
        {
            "results": [
                {"passed": False, "score": 0.3, "task": "security"},
                {"passed": True, "score": 0.9, "task": "reasoning"},
                {"passed": True, "score": 0.8, "task": "behavior",
                 "details": {"verbosity": {"tendency": "moderate"}}},
            ],
        },
        # All rounder
        {
            "results": [
                {"passed": True, "score": 0.9, "task": "security"},
                {"passed": True, "score": 0.95, "task": "reasoning"},
                {"passed": True, "score": 0.85, "task": "behavior",
                 "details": {"verbosity": {"tendency": "moderate"}}},
            ],
        },
    ]
    
    for i, demo in enumerate(demo_results):
        name, reason = generate_name(demo)
        print(f"Profile {i+1}: {name}")
        print(f"  {reason}\n")
