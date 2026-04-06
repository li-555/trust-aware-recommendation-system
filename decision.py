def normalize_entropy(entropy):
    return 1 / (1 + entropy)


def confidence_adjustment(model_conf, entropy):
    return model_conf * (1 / (1 + entropy))

from collections import Counter
from uncertainty.entropy import compute_uncertainty
from uncertainty.calibration import normalize_entropy, confidence_adjustment
from config import *

def decision(results):
    if len(results) < MIN_VALID_SAMPLES:
        return {"status": "FAILED", "reason": "Insufficient valid samples"}

    entropy, variation = compute_uncertainty(results)

    labels = [r["sentiment"] for r in results]
    pred = Counter(labels).most_common(1)[0][0]

    model_conf = sum([r["confidence"] for r in results]) / len(results)

    confidence = normalize_entropy(entropy)
    adjusted_conf = confidence_adjustment(model_conf, entropy)

    status = "ACCEPTED" if entropy < ENTROPY_THRESHOLD else "ABSTAIN"

    return {
        "prediction": pred,
        "confidence": round(confidence, 3),
        "adjusted_confidence": round(adjusted_conf, 3),
        "entropy": round(entropy, 3),
        "variation": round(variation, 3),
        "status": status
    }