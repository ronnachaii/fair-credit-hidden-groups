"""ตัวชี้วัดการตัดสินใจและช่องว่างระหว่างกลุ่มจริง"""
import json
import numpy as np
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score)
from .data import reference_groups as acs_groups
from .hmda import reference_groups as hmda_groups, UNKNOWN


def group_metrics(y, prediction, group, min_size=1):
    """EO = max(ช่วง TPR, ช่วง FPR); ไม่แทนอัตราที่ไม่มีตัวหารด้วยศูนย์"""
    details, tprs, fprs, positives = {}, [], [], []
    for value in np.unique(group):
        mask = group == value
        if mask.sum() < min_size:
            continue
        yy, pp = y[mask], prediction[mask]
        tpr = float(pp[yy == 1].mean()) if (yy == 1).any() else np.nan
        fpr = float(pp[yy == 0].mean()) if (yy == 0).any() else np.nan
        details[str(value)] = {"n": int(mask.sum()), "accuracy": float((yy == pp).mean()),
                              "tpr": tpr if np.isfinite(tpr) else None,
                              "fpr": fpr if np.isfinite(fpr) else None,
                              "positive_rate": float(pp.mean())}
        if np.isfinite(tpr):
            tprs.append(tpr)
        if np.isfinite(fpr):
            fprs.append(fpr)
        positives.append(float(pp.mean()))
    def gap(values):
        return max(values) - min(values) if len(values) >= 2 else np.nan
    return {"eo_gap": max(gap(tprs), gap(fprs)), "tpr_gap": gap(tprs),
            "fpr_gap": gap(fprs), "dp_difference": gap(positives),
            "worst_group_accuracy": min((v["accuracy"] for v in details.values()), default=np.nan),
            "n_eligible_groups": len(details), "group_accuracy": details}


def evaluate(y, probability, sensitive, min_detail=30):
    """คอลัมน์ fairness หลักใช้ intersection เพศ × White/Non-white"""
    prediction = (probability >= 0.5).astype(int)
    result = {"accuracy": accuracy_score(y, prediction),
              "precision": precision_score(y, prediction, zero_division=0),
              "recall": recall_score(y, prediction, zero_division=0),
              "f1": f1_score(y, prediction, zero_division=0),
              "auroc": roc_auc_score(y, probability)}
    refs = hmda_groups(sensitive) if "race_eth" in sensitive else acs_groups(sensitive)
    result["positive_rate"] = float(prediction.mean())
    for name, group in refs.items():
        eligible = group != UNKNOWN
        result[f"excluded_unknown_{name}"] = int((~eligible).sum())
        scores = group_metrics(y[eligible], prediction[eligible], group[eligible], min_detail)
        result[f"excluded_small_{name}"] = int(eligible.sum() - sum(v["n"] for v in scores["group_accuracy"].values()))
        result[f"approval_rate_gap_{name}"] = scores["dp_difference"]
        for metric, value in scores.items():
            result[f"{metric}_{name}"] = json.dumps(value, ensure_ascii=False) if isinstance(value, dict) else value
        if name == "intersection":
            for metric in ["eo_gap", "tpr_gap", "fpr_gap", "dp_difference", "worst_group_accuracy"]:
                result[metric] = scores[metric]
    return result
