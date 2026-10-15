"""อัปเดตน้ำหนักกลุ่มแบบ exponentiated gradient ของ group DRO"""
import numpy as np
import torch


def balanced_cluster_weights(clusters, y):
    """w_i=n_c/(จำนวนคลาสที่มีใน c × n_cy); แต่ละคลาสมีมวลเท่ากันภายใน cluster"""
    weights = np.ones(len(y), dtype=np.float32)
    for cluster in np.unique(clusters):
        mask = clusters == cluster
        labels, counts = np.unique(y[mask], return_counts=True)
        for label, count in zip(labels, counts):
            weights[mask & (y == label)] = mask.sum() / (len(labels) * count)
    return weights


def validation_groups(clusters, y=None, definition='c'):
    """c ใช้ cluster อย่างเดียว; cy เพิ่ม y โดย Unknown ยังคงถูกตัดออกสำหรับ oracle"""
    if definition == 'c':
        return np.asarray(clusters).copy()
    if definition != 'cy' or y is None:
        raise ValueError('cy ต้องมี y และ definition ต้องเป็น c หรือ cy')
    return np.array(['Unknown' if str(c) == 'Unknown' else f'{c}|y={label}'
                     for c, label in zip(clusters, y)])


def make_dro_groups(x, clusters, min_size=50, definition='c', y=None):
    """รวมกลุ่ม c โดยไม่ดู y; cy รวมได้เฉพาะคลาสเดียวกันตามรอบก่อน"""
    if definition not in ('c', 'cy') or (definition == 'cy' and y is None):
        raise ValueError('นิยามกลุ่มไม่ถูกต้อง')
    labels = np.zeros(len(clusters), dtype=int) if definition == 'c' else y
    groups, details = merge_small_groups(x, labels, clusters, min_size)
    if definition == 'c':
        for row in details['mapping']:
            row.pop('y')
    details['group_definition'] = definition
    return groups, details


def merge_small_groups(x, y, clusters, min_size=50):
    """รวม cluster × y ที่เล็กด้วยระยะศูนย์กลาง train ในคลาสเดียวกันเท่านั้น"""
    pairs, groups = np.unique(np.column_stack([clusters, y]), axis=0, return_inverse=True)
    initial = groups.copy()
    active = {g: {'label': pair[1], 'n': int((groups == g).sum()),
                  'center': x[groups == g].mean(axis=0)} for g, pair in enumerate(pairs)}
    while True:
        small = [g for g, d in active.items() if d['n'] < min_size and
                 any(h != g and e['label'] == d['label'] for h, e in active.items())]
        if not small:
            break
        source = min(small, key=lambda g: (active[g]['n'], g))
        a = active[source]
        same_class = [g for g, d in active.items() if g != source and d['label'] == a['label']]
        target = min(same_class, key=lambda g: (float(np.sum((active[g]['center'] - a['center'])**2)), g))
        b = active[target]
        b['center'] = (b['center'] * b['n'] + a['center'] * a['n']) / (b['n'] + a['n'])
        b['n'] += a['n']
        groups[groups == source] = target
        del active[source]
    _, merged = np.unique(groups, return_inverse=True)
    details = {'n_groups_before': len(pairs), 'n_groups_after': len(active),
               'min_size': min_size, 'fit_split': 'train',
               'mapping': [{'cluster': int(c), 'y': int(label),
                            'dro_group': int(merged[np.flatnonzero(initial == g)[0]])}
                           for g, (c, label) in enumerate(pairs)],
               'group_sizes': np.bincount(merged).tolist()}
    # ถ้าทั้งคลาสมีน้อยกว่าเกณฑ์ จะเหลือหนึ่งกลุ่มและรายงาน ไม่รวมข้ามคลาส
    details['undersized_remaining'] = sum(n < min_size for n in details['group_sizes'])
    return merged, details


def group_dro_loss(losses, groups, log_weights, eta, group_counts=None, adjustment=0.0):
    """เฉลี่ย loss ในแต่ละกลุ่มก่อนถ่วงน้ำหนัก กลุ่มว่างไม่ทำให้ NaN"""
    means = torch.zeros_like(log_weights)
    present = torch.zeros_like(log_weights, dtype=torch.bool)
    for group in groups.unique():
        present[group] = True
        means[group] = losses[groups == group].mean()
    with torch.no_grad():
        adjusted = means.detach().clone()
        if adjustment:
            if group_counts is None:
                raise ValueError('ต้องใช้ขนาดกลุ่มจาก train ทั้งชุดสำหรับ C/sqrt(n_g)')
            adjusted[present] += adjustment / group_counts[present].sqrt()
        # กลุ่มที่ไม่อยู่ใน batch ไม่ถูกเพิ่ม loss สมมติ
        log_weights.add_(eta * adjusted)
        log_weights.sub_(torch.logsumexp(log_weights, dim=0))
    weights = torch.softmax(log_weights, dim=0) * present
    weights = weights / weights.sum()
    return (weights * means).sum()
