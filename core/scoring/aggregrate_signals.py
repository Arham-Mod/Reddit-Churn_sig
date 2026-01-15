from collections import defaultdict
from typing import List, Dict

SIGNAL_WEIGHTS = {
    "explicit_exit_intent": 3.0,
    "trust_erosion": 2.5,
    "support_failure": 2.0,
    "pricing_dissatisfaction": 1.8,
    "churn_threat": 1.6,
    "feature_complaint": 1.2,
    "competitor_comparison": 1.0,
    "degraded_experience": 1.0
}

def aggregate_feature_scores(extractions: List[Dict]) -> Dict:
    """
    Aggregate churn signals by feature.
    """

    features = defaultdict(lambda: {
        "score": 0.0,
        "count": 0,
        "evidence": [],
        "root_causes": set()
    })

    for item in extractions:
        signals = item.get("signals", [])
        feats = item.get("features", [])
        root = item.get("root_cause")

        for f in feats:
            feature_name = f.get("canonical") or f.get("raw")
            feature_conf = f.get("confidence", 0.5)

            for s in signals:
                weight = SIGNAL_WEIGHTS.get(s["id"], 1.0)
                features[feature_name]["score"] += (
                    weight * s["confidence"] * feature_conf
                )

            features[feature_name]["count"] += 1

            if root:
                features[feature_name]["root_causes"].add(root)

            if len(features[feature_name]["evidence"]) < 5:
                features[feature_name]["evidence"].append(item)

    return dict(features)
