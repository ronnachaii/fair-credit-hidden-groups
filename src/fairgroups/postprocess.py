"""ปรับเกณฑ์บน validation เท่านั้น ไม่เปลี่ยนคะแนนเดิม และไม่พึ่ง fairlearn"""
import hashlib
import time
import numpy as np
import pandas as pd
from .efficiency import ResourceMonitor
from .metrics import evaluate


class XRandomGroups:
    """กลุ่มควบคุมจาก hash ของ x: รายเดิมได้กลุ่มเดิม ไม่อ่าน y/ประชากร"""
    def fit(self, x, ids, k, seed):
        self.k, self.seed = k, seed
        self.fit_ids_ = np.asarray(ids).copy()
        return self

    def predict(self, x):
        key = str(self.seed).encode()
        return np.array([int.from_bytes(hashlib.blake2b(row.tobytes(), key=key,
                         digest_size=8).digest(), 'little') % self.k
                         for row in np.asarray(x, dtype='<f4')])


def _span(values):
    values = np.asarray(values)
    values = values[np.isfinite(values)]
    return float(np.ptp(values)) if len(values) > 1 else 0.


class ValidationThresholds:
    """Parity ใช้ช่วงอัตราอนุมัติ; EO ใช้ค้นทีละกลุ่ม จึงไม่รับรอง optimum EO"""
    def __init__(self, objective='parity', min_group=50, tolerance=.02):
        if objective not in ('parity', 'eo'):
            raise ValueError('objective ต้องเป็น parity หรือ eo')
        self.objective, self.min_group, self.tolerance = objective, min_group, tolerance

    def _tables(self, p, y, groups):
        tables = []
        for g in self.groups_:
            mask = groups == g
            pg, yg = p[mask], y[mask]
            # ใส่ 0.5 ไว้ก่อนเพื่อคงเกณฑ์เดิมเมื่อผลเสมอกัน
            thresholds = np.array([.5])
            if len(pg) >= self.min_group:
                extra = np.unique(np.r_[np.arange(.05, .951, .01),
                    np.quantile(pg, np.linspace(0, 1, 101)), np.nextafter(pg.max(), np.inf)])
                thresholds = np.r_[.5, extra[extra != .5]]
            pred = pg[:, None] >= thresholds
            tables.append({'threshold': thresholds, 'n': len(pg),
                'correct': (pred == yg[:, None]).sum(axis=0), 'rate': pred.mean(axis=0),
                'tpr': pred[yg == 1].mean(axis=0) if (yg == 1).any() else np.full(len(thresholds), np.nan),
                'fpr': pred[yg == 0].mean(axis=0) if (yg == 0).any() else np.full(len(thresholds), np.nan)})
        return tables

    def _stats(self, indices):
        values = {key: [tab[key][i] for tab, i in zip(self.tables_, indices)]
                  for key in ['correct', 'rate', 'tpr', 'fpr']}
        return {'accuracy': float(sum(values['correct']) / self.n_),
                'approval_gap': _span(values['rate']),
                'eo_gap': max(_span(values['tpr']), _span(values['fpr']))}

    def _parity(self):
        """แต่ละช่วงเลือกจำนวนทายถูกสูงสุดต่อกลุ่ม แล้วตรวจงบ accuracy รวม"""
        lower = np.unique(np.concatenate([t['rate'] for t in self.tables_]))
        def search(width):
            correct, choices = np.zeros(len(lower)), []
            for tab in self.tables_:
                valid = (tab['rate'][None, :] >= lower[:, None] - 1e-12) & (
                         tab['rate'][None, :] <= lower[:, None] + width + 1e-12)
                scores = np.where(valid, tab['correct'][None, :], -self.n_ * 2)
                idx = scores.argmax(axis=1)
                correct += scores[np.arange(len(lower)), idx]
                choices.append(idx)
            feasible = np.flatnonzero(correct >= self.required_correct_)
            if not len(feasible):
                return None
            best = feasible[np.argmax(correct[feasible])]
            return np.array([c[best] for c in choices])
        lo, hi, best = 0., 1., search(1.)
        for _ in range(20):
            mid = (lo + hi) / 2
            candidate = search(mid)
            if candidate is None:
                lo = mid
            else:
                hi, best = mid, candidate
        return best

    def _eo(self, parity):
        """เริ่มจากเกณฑ์เดิมและ parity; รับเฉพาะการขยับที่ผ่าน guard"""
        def rank(indices):
            s = self._stats(indices)
            return (s['eo_gap'], s['approval_gap'], -s['accuracy'])
        candidates = []
        for start in [np.zeros(len(self.groups_), dtype=int), parity]:
            indices = start.copy()
            for _ in range(10):
                before = indices.copy()
                for j, tab in enumerate(self.tables_):
                    correct = sum(t['correct'][i] for t, i in zip(self.tables_, indices)) - tab['correct'][indices[j]]
                    feasible = correct + tab['correct'] >= self.required_correct_
                    keys = []
                    for key in ['tpr', 'fpr', 'rate']:
                        other = np.array([t[key][indices[h]] for h, t in enumerate(self.tables_) if h != j])
                        other = other[np.isfinite(other)]
                        value = tab[key]
                        if len(other):
                            span = np.maximum(np.nan_to_num(value, nan=other.max()), other.max()) - np.minimum(
                                   np.nan_to_num(value, nan=other.min()), other.min())
                        else:
                            span = np.zeros(len(value))
                        keys.append(span)
                    eo = np.maximum(keys[0], keys[1])
                    order = np.lexsort((np.arange(len(eo)), -tab['correct'], keys[2], eo, ~feasible))
                    trial = indices.copy(); trial[j] = order[0]
                    if feasible[order[0]] and rank(trial) < rank(indices):
                        indices = trial
                if np.array_equal(before, indices):
                    break
            candidates.append(indices)
        return min(candidates, key=rank)

    def fit(self, probability, y, groups, ids, *, split='validation'):
        if split != 'validation':
            raise ValueError('หาเกณฑ์ได้เฉพาะ validation')
        p, y, groups = np.asarray(probability), np.asarray(y), np.asarray(groups)
        if not (len(p) == len(y) == len(groups) == len(ids)) or not len(p):
            raise ValueError('ขนาด validation ไม่ตรงกันหรือว่าง')
        if not np.isfinite(p).all() or not np.isin(y, [0, 1]).all():
            raise ValueError('คะแนนต้อง finite และ y เป็น 0/1')
        self.fit_ids_, self.fit_split_ = np.asarray(ids).copy(), split
        self.groups_, self.n_ = np.unique(groups), len(p)
        self.baseline_accuracy_ = float(((p >= .5) == y).mean())
        self.accuracy_floor_ = self.baseline_accuracy_ - self.tolerance
        self.required_correct_ = int(np.ceil(self.accuracy_floor_ * len(y) - 1e-9))
        self.tables_ = self._tables(p, y, groups)
        indices = self._parity()
        if self.objective == 'eo':
            indices = self._eo(indices)
        self.thresholds_ = {g: float(t['threshold'][i]) for g, t, i in zip(self.groups_, self.tables_, indices)}
        self.counts_ = {g: int(t['n']) for g, t in zip(self.groups_, self.tables_)}
        self.validation_ = self._stats(indices)
        assert self.validation_['accuracy'] >= self.accuracy_floor_ - 1e-12
        return self

    def predict(self, probability, groups):
        thresholds = np.array([self.thresholds_.get(g, .5) for g in groups])
        return (np.asarray(probability) >= thresholds).astype(int)


def selection_key(row):
    """อ่านเฉพาะผล validation ของกลุ่มค้นพบ; ไม่รับผล test/กลุ่มจริง"""
    return (not row['accuracy_guard_passed'], row['validation_approval_gap'],
            -row['validation_accuracy'], row['validation_eo_gap'], row['method'], row['objective'])


def fit_candidates(base, probabilities, val, methods, config, seed):
    """เลือกทุกตัวให้เสร็จก่อนส่ง test เข้ามาประเมิน"""
    candidates = []
    for method, rep, k, labels in methods:
        for objective in ['parity', 'eo']:
            with ResourceMonitor() as monitor:
                model = ValidationThresholds(objective, config.min_dro_group,
                    config.selection_accuracy_tolerance).fit(probabilities, val['y'], labels['val'], val['ids'])
            s = model.validation_
            row = {'seed': seed, 'base': base, 'method': method, 'representation': rep, 'k': k,
                'objective': objective, 'fit_split': 'validation', 'group_definition': 'c',
                'uses_demographics_at_inference': rep == 'oracle',
                'validation_accuracy': s['accuracy'], 'validation_approval_gap': s['approval_gap'],
                'validation_eo_gap': s['eo_gap'], 'validation_accuracy_floor': model.accuracy_floor_,
                'erm_validation_accuracy': model.baseline_accuracy_,
                'accuracy_guard_passed': s['accuracy'] >= model.accuracy_floor_ - 1e-12,
                'threshold_fit_seconds': monitor.seconds, 'threshold_peak_process_rss_mb': monitor.peak_mb,
                'threshold_peak_rss_increase_mb': (monitor.peak - monitor.peak_start) / 1024**2,
                'n_validation_groups': len(model.groups_),
                'n_frozen_small_groups': sum(n < config.min_dro_group for n in model.counts_.values()),
                'selected_without_demographics': False, 'proposed_selected': False}
            candidates.append((row, model, labels))
    for flag, eligible in [
        ('selected_without_demographics', [c for c in candidates if c[0]['representation'] not in ['oracle', 'random']]),
        ('proposed_selected', [c for c in candidates if c[0]['representation'] in ['raw', 'scarf']])]:
        min(eligible, key=lambda c: selection_key(c[0]))[0][flag] = True
    return candidates


def evaluate_candidates(candidates, probability, test, min_detail):
    """ขั้นนี้อ่าน test เพื่อวัดผลเท่านั้น ไม่มีการ fit หรือเลือกเพิ่ม"""
    rows, thresholds = [], []
    for metadata, model, labels in candidates:
        start = time.perf_counter()
        prediction = model.predict(probability, labels['test'])
        seconds = time.perf_counter() - start
        rows.append({**metadata, **evaluate(test['y'], probability, test['s'], min_detail, prediction),
            'threshold_inference_seconds_per_1000': seconds * 1000 / len(prediction)})
        for g, threshold in model.thresholds_.items():
            thresholds.append({**{k: metadata[k] for k in ['seed', 'base', 'method', 'objective',
                'proposed_selected', 'selected_without_demographics']}, 'group': g, 'threshold': threshold,
                'n_validation': model.counts_[g], 'frozen_small_group': model.counts_[g] < model.min_group,
                'fit_split': model.fit_split_, 'unseen_group_threshold': .5})
    return rows, thresholds
