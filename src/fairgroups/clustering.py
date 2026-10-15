"""จัดกลุ่มและวัดความตรงกับกลุ่มอ้างอิงหลัง fit เท่านั้น"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import (adjusted_rand_score, normalized_mutual_info_score,
                             silhouette_score, davies_bouldin_score)
from .data import reference_groups


def discover(representation, ids, sensitive, k, seed):
    """ข้อมูลประชากรใช้คำนวณ ARI/NMI เท่านั้น ไม่ส่งให้ k-means"""
    model = KMeans(n_clusters=k, n_init=10, random_state=seed)
    clusters = model.fit_predict(representation)
    model.fit_ids_ = np.asarray(ids).copy()
    scores = {"silhouette": float(silhouette_score(representation, clusters,
               sample_size=min(1000, len(clusters)), random_state=seed)),
              "davies_bouldin": float(davies_bouldin_score(representation, clusters)),
              "reconstruction_error": np.nan}
    for name, values in reference_groups(sensitive).items():
        scores[f"ari_{name}"] = adjusted_rand_score(values, clusters)
        scores[f"nmi_{name}"] = normalized_mutual_info_score(values, clusters)
    return clusters, scores, model


def cross_label_groups(clusters, y):
    """DRO เห็น cluster × y เฉพาะแถวที่มีป้ายกำกับ"""
    _, contiguous = np.unique(np.column_stack([clusters, y]), axis=0, return_inverse=True)
    return contiguous
