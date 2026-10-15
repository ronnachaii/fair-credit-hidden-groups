"""จัดกลุ่ม train ภายในคลาส และทำนายรายใหม่โดยไม่รู้ y"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, silhouette_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler
from .hmda import reference_groups, UNKNOWN
from .models import predict_mlp
import torch


class ClassClusters:
    """k ต่อคลาส รวม 2k กลุ่ม; ตอนใช้จริงเลือกศูนย์กลางที่ใกล้สุดข้ามคลาส"""
    def fit(self, x, y, ids, k, seed):
        self.models_, self.centers_, self.labels_ = [], [], np.zeros(len(y), dtype=int)
        for label in [0,1]:
            mask = y == label
            km = KMeans(n_clusters=k,n_init=10,random_state=seed).fit(x[mask])
            self.models_.append(km); self.centers_.append(km.cluster_centers_)
            self.labels_[mask] = label*k + km.labels_
        self.centers_ = np.vstack(self.centers_).astype(np.float32)
        self.fit_ids_ = np.asarray(ids).copy()
        return self

    def predict(self, x):
        from sklearn.metrics import pairwise_distances_argmin
        return pairwise_distances_argmin(x, self.centers_)


class GeoGroups:
    """ใช้ minority percent เฉพาะ baseline นี้ ขอบ quantile มาจาก train"""
    def fit(self, values, ids, k=4):
        self.median_ = float(np.nanmedian(values))
        self.edges_ = np.unique(np.quantile(np.nan_to_num(values,nan=self.median_), np.arange(1,k)/k))
        self.fit_ids_ = np.asarray(ids).copy()
        return self
    def predict(self, values):
        return np.digitize(np.nan_to_num(values,nan=self.median_),self.edges_)


def hidden(model,x):
    model.eval()
    with torch.no_grad():
        return np.concatenate([model.layers[:-1](torch.as_tensor(x[i:i+2048])).numpy() for i in range(0,len(x),2048)])


def group_scores(x, labels, s, seed):
    out = {'n_clusters':len(np.unique(labels)), 'silhouette':np.nan, 'davies_bouldin':np.nan}
    if 1 < len(np.unique(labels)) < len(labels):
        out.update(silhouette=float(silhouette_score(x,labels,sample_size=min(1000,len(labels)),random_state=seed)),
                   davies_bouldin=float(davies_bouldin_score(x,labels)))
    for name, group in reference_groups(s).items():
        keep = group != UNKNOWN
        out[f'ari_{name}'] = adjusted_rand_score(group[keep],labels[keep])
        out[f'nmi_{name}'] = normalized_mutual_info_score(group[keep],labels[keep])
        out[f'alignment_excluded_{name}'] = int((~keep).sum())
    return out


def fit_hbac(x, error, ids, seed, k=4):
    """ใช้ API จริงของแพ็กเกจ; error สูงคือคุณภาพต่ำ จึงส่ง -error"""
    from unsupervised_bias_detection.cluster import BiasAwareHierarchicalKMeans
    model = BiasAwareHierarchicalKMeans(bahc_max_iter=k-1, bahc_min_cluster_size=max(20,len(x)//200),
                                       random_state=seed,n_init=5)
    model.fit(x, -error)
    model.fit_ids_ = np.asarray(ids).copy()
    return model
