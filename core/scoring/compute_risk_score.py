from typing import List, Dict


SEVERITY_WEIGHTS = {
    "low": 1,
    "medium": 2,
    "high": 3
}

MAX_SEVERITY_WEIGHT = max(SEVERITY_WEIGHTS.values())  # = 3


def get_risk_level(score: float) -> str:
    if score <= 2:
        return "Low"
    elif score <= 4:
        return "Mild"
    elif score <= 6:
        return "Moderate"
    elif score <= 8:
        return "High"
    else:
        return "Critical"


def get_score_explanation(score: float) -> str:
    if score <= 2:
        return "Minor and infrequent complaints with low churn impact."
    elif score <= 4:
        return "Noticeable dissatisfaction affecting a small subset of users."
    elif score <= 6:
        return "Repeated complaints indicating growing frustration over time."
    elif score <= 8:
        return "Widespread dissatisfaction strongly associated with churn risk."
    else:
        return "Dominant issue with explicit signals of cancellation or switching."


def compute_churn_scores(
    aggregated_issues: List[Dict]
) -> List[Dict]:
    """
    Compute normalized churn risk scores (0–10) for aggregated churn issues.
    """

    scored_issues: List[Dict] = []

    for issue in aggregated_issues:
        severity_dist = issue.get("severity_distribution", {})
        num_posts = issue.get("num_posts", 0)

        if num_posts == 0:
            continue

        # Step 1: weighted severity sum
        weighted_sum = 0
        for severity, count in severity_dist.items():
            weight = SEVERITY_WEIGHTS.get(severity, 0)
            weighted_sum += weight * count

        # Step 2: average severity per post (0–3)
        avg_severity = weighted_sum / num_posts

        # Step 3: normalize to 0–10 scale
        normalized_score = round((avg_severity / MAX_SEVERITY_WEIGHT) * 10, 2)

        issue_with_score = issue.copy()
        issue_with_score["churn_score"] = normalized_score
        issue_with_score["risk_level"] = get_risk_level(normalized_score)
        issue_with_score["score_explanation"] = get_score_explanation(normalized_score)

        scored_issues.append(issue_with_score)

    # Sort by churn_score descending
    scored_issues.sort(
        key=lambda x: x["churn_score"],
        reverse=True
    )

    return scored_issues
