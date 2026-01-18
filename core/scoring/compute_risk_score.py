from typing import List, Dict


SEVERITY_WEIGHTS = {
    "low": 1,
    "medium": 2,
    "high": 3
}


def compute_churn_scores(
    aggregated_issues: List[Dict]
) -> List[Dict]:
    """
    Compute churn risk scores for aggregated churn issues.

    Input:
        aggregated_issues: Output of aggregate_churn_issues()

    Output:
        Sorted list of churn issues with churn_score added
    """

    scored_issues: List[Dict] = []

    for issue in aggregated_issues:
        severity_dist = issue.get("severity_distribution", {})
        num_posts = issue.get("num_posts", 0)

        if num_posts == 0:
            continue

        score = 0
        for severity, count in severity_dist.items():
            weight = SEVERITY_WEIGHTS.get(severity, 0)
            score += weight * count

        churn_score = round(score / num_posts, 2)

        issue_with_score = issue.copy()
        issue_with_score["churn_score"] = churn_score

        scored_issues.append(issue_with_score)

    # Sort by churn_score descending
    scored_issues.sort(
        key=lambda x: x["churn_score"],
        reverse=True
    )

    return scored_issues
