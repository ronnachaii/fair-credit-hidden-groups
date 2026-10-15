"""อัปเดตน้ำหนักกลุ่มแบบ exponentiated gradient ของ group DRO"""
import torch


def group_dro_loss(losses, groups, log_weights, eta):
    """เฉลี่ย loss ในแต่ละกลุ่มก่อนถ่วงน้ำหนัก กลุ่มว่างไม่ทำให้ NaN"""
    means = torch.zeros_like(log_weights)
    present = torch.zeros_like(log_weights, dtype=torch.bool)
    for group in groups.unique():
        present[group] = True
        means[group] = losses[groups == group].mean()
    with torch.no_grad():
        log_weights.add_(eta * means.detach())
        log_weights.sub_(torch.logsumexp(log_weights, dim=0))
    weights = torch.softmax(log_weights, dim=0) * present
    weights = weights / weights.sum()
    return (weights * means).sum()
