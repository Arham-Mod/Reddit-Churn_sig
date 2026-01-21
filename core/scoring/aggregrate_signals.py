from typing import List, Dict, Tuple
from collections import defaultdict


def aggregrate_churn_issues(
    discussion_results: List[Dict]
) -> List[Dict]:
    """
    Aggregate post-wise churn issues into feature-level churn signals.

    Input:
        discussion_results: List of dicts returned by analyze_discussion_for_churn()

    Output:
        List of aggregated churn issue dicts
    """

    # Group by (affected_feature, problem_type)
    grouped = {}

    for result in discussion_results:
        post_id = result.get("post_id")
        issues = result.get("issues", [])

        for issue in issues:
            feature = issue.get("affected_feature")
            problem_type = issue.get("problem_type")
            severity = issue.get("churn_severity")
            quotes = issue.get("supporting_quotes", [])

            if not feature or not problem_type or not severity:
                continue

            key: Tuple[str, str] = (feature, problem_type)

            if key not in grouped:
                grouped[key] = {
                    "affected_feature": feature,
                    "problem_type": problem_type,
                    "post_ids": set(),
                    "severity_distribution": {
                        "low": 0,
                        "medium": 0,
                        "high": 0
                    },
                    "example_quotes": []
                }

            grouped[key]["post_ids"].add(post_id)

            if severity in grouped[key]["severity_distribution"]:
                grouped[key]["severity_distribution"][severity] += 1

            # Collect quotes (cap later)
            grouped[key]["example_quotes"].extend(quotes)

    # Finalize structure
    aggregated_issues: List[Dict] = []

    for data in grouped.values():
        aggregated_issues.append({
            "affected_feature": data["affected_feature"],
            "problem_type": data["problem_type"],
            "num_posts": len(data["post_ids"]),
            "severity_distribution": data["severity_distribution"],
            "example_quotes": data["example_quotes"][:3]
        })

    return aggregated_issues
