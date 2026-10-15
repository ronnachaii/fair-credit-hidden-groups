"""สร้างรายงานและกราฟจาก CSV ที่บันทึกแล้วเท่านั้น"""
import os
from pathlib import Path
import numpy as np
import pandas as pd


def markdown_table(frame, groups, metrics):
    """ไม่ใช้ tabulate เพื่อลดแพ็กเกจที่ต้องติดตั้ง"""
    rows = ["| " + " | ".join(groups + metrics) + " |",
            "| " + " | ".join(["---"] * (len(groups) + len(metrics))) + " |"]
    for key, part in frame.groupby(groups, sort=True, dropna=False):
        key = key if isinstance(key, tuple) else (key,)
        cells = [str(v) for v in key]
        for metric in metrics:
            values = part[metric].dropna()
            if len(values) > 1:
                cells.append(f"{values.mean():.4f} ± {values.std(ddof=1):.4f}")
            else:
                cells.append(f"{values.mean():.4f}" if len(values) else "N/A")
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join(rows)


def generate_reports(root):
    """โหลดผลจากดิสก์ใหม่ ไม่ฝังตัวเลขผลทดลองลงในข้อความ"""
    root = Path(root)
    results = pd.read_csv(root / "pilot_results.csv")
    clusters = pd.read_csv(root / "clustering_results.csv")
    resources = pd.read_csv(root / "representation_resources.csv")
    groups = ["selection", "label_fraction", "method"]
    text = ["# ผลนำร่อง ACS CA 2018", "",
            "ค่าทุกตารางเป็น mean ± sample SD ข้าม seed และอ่านจาก CSV เท่านั้น", "",
            "selection=average เป็นผลหลัก; worst_group ใช้เพศ/เชื้อชาติจริงใน validation เพื่อเลือก checkpoint", "",
            "EO gap และ worst-group หลักใช้เพศ × White/Non-white; เกณฑ์ทำนาย 0.5 ทุกวิธี", "",
            "## ความแม่นยำและความเป็นธรรม", "",
            markdown_table(results, groups, ["accuracy", "precision", "recall", "f1", "auroc",
                           "eo_gap", "dp_difference", "worst_group_accuracy"]), "",
            "## ความตรงของกลุ่ม (วัดบนข้อมูล train ที่ใช้ค้นหากลุ่ม)", "",
            "raw/scarf ใช้ train ทั้งหมดโดยไม่ใช้ y; error ใช้ OOF เฉพาะ train ที่มีป้ายกำกับตามงบ", "",
            "discovery_label_fraction=0 หมายถึงไม่ใช้ป้ายกำกับ ไม่ใช่ไม่มีข้อมูลฝึก", "",
            markdown_table(clusters, ["representation", "discovery_label_fraction", "k"],
                           ["silhouette", "davies_bouldin", "ari_sex", "nmi_sex", "ari_race", "nmi_race",
                            "ari_intersection", "nmi_intersection"]), "",
            "Reconstruction error: N/A เพราะ SCARF ไม่มี decoder", "",
            "## ประสิทธิภาพระบบ", "",
            "train_seconds รวม preprocessing + discovery ที่นำกลับใช้ร่วมกัน + การฝึกตัวตัดสินใจของวิธีนั้น "
            "จึงห้ามนำเวลาแต่ละแถวมารวมเป็นเวลารันทั้งชุด; peak_memory_mb เป็น RSS รวมของ Python ที่สุ่มทุก 10 ms", "",
            markdown_table(results, groups, ["train_seconds", "decision_train_seconds",
                           "inference_seconds_per_1000", "peak_memory_mb", "parameters", "flops_per_row",
                           "tree_count", "leaf_count"]), "",
            "## ต้นทุนการค้นหา representation", "",
            "SCARF encoder แยกจาก projection head; FLOPs นับเฉพาะ Linear ตาม 2×in×out", "",
            markdown_table(resources, ["representation", "discovery_label_fraction"],
                           ["discovery_train_seconds", "inference_seconds_per_1000", "peak_memory_mb", "parameters", "flops_per_row",
                            "pretraining_parameters", "pretraining_flops_per_row"]), "",
            "## ความสัมพันธ์ของความตรงของกลุ่มกับผลความเป็นธรรม", "",
            "ค่าสหสัมพันธ์เชิงสำรวจจาก cluster methods เท่านั้น ยังไม่ใช่ข้อสรุปเชิงเหตุและผล", ""]
    relation_rows = []
    for (selection, fraction), part in results[results.representation.isin(["raw", "scarf", "error"]) &
                                                    results.method.str.startswith("GDRO-")].groupby(["selection", "label_fraction"]):
        for metric in ["ari_intersection", "nmi_intersection"]:
            relation_rows.append({"selection": selection, "label_fraction": fraction, "alignment": metric,
                "pearson_worst_group": part[metric].corr(part.worst_group_accuracy),
                "pearson_eo_gap": part[metric].corr(part.eo_gap), "n": len(part)})
    relation = pd.DataFrame(relation_rows)
    relation.to_csv(root / "alignment_fairness_correlations.csv", index=False)
    text += [markdown_table(relation, ["selection", "label_fraction", "alignment"],
                            ["pearson_worst_group", "pearson_eo_gap"]), "",
             "## ข้อจำกัด", "",
             "- เป็น pilot ขนาดย่อและ epochs น้อย ผลไม่ได้รับประกันว่าจะลดช่องว่างได้ทุกวิธี", 
             "- error เป็น label-assisted discovery จึงแยกจาก raw/scarf ที่ไม่ใช้ป้ายกำกับ",
             "- กลุ่มละเอียดขนาดต่ำกว่าเกณฑ์ถูกตัดออกจาก fairness แบบละเอียดเท่านั้น ดูจำนวนใน CSV",
             "- ใช้ POBP ซึ่งอาจเป็น proxy เชื้อชาติ; oracle ใช้ข้อมูลประชากร train และเป็นเพียงตัวเทียบ",
             "- การแบ่งข้อมูล stratified ใช้กลุ่มจริงเพื่อออกแบบการประเมิน; ตัวฝึกหลักไม่รับข้อมูลนั้น",
             "- ยังไม่ยืนยันเวลาจริงบน Colab; ARL และ Gradio อยู่ใน TODO", ""]
    # EO ต่ำอาจเกิดจากทายคลาสเดียว จึงตรวจจากอัตราทายบวกที่เก็บจริงใน CSV
    for (selection, fraction), part in results[results.method == "JTT"].groupby(["selection", "label_fraction"]):
        rates = []
        for raw in part.group_accuracy_intersection:
            import json
            groups = json.loads(raw)
            rates.append(sum(g["n"] * g["positive_rate"] for g in groups.values()) /
                         sum(g["n"] for g in groups.values()))
        if any(rate > 0.98 or rate < 0.02 for rate in rates):
            text.append(f"- ตรวจพบ JTT ทำนายกระจุกคลาสเดียวอย่างน้อยหนึ่ง seed: selection={selection}, "
                        f"labels={fraction:g}, อัตราทายบวกเฉลี่ย={np.mean(rates):.4f}; "
                        "EO gap ต่ำในกรณีนี้ไม่ใช่หลักฐานว่าตัดสินใจได้ดีขึ้น ต้องอ่าน accuracy/recall ควบคู่")
    text.append("")
    (root / "pilot_summary.md").write_text("\n".join(text), encoding="utf-8")
    make_figures(results, clusters, root)


def make_figures(results, clusters, root):
    """กราฟแยกกติกาเลือกโมเดลเพื่อไม่ปะปนการใช้ข้อมูลประชากร"""
    os.environ.setdefault("MPLCONFIGDIR", str(root / ".matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    figure_dir = root / "figures"
    figure_dir.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for metric, ax in zip(["ari_intersection", "nmi_intersection"], axes):
        for (rep, frac), part in clusters.groupby(["representation", "discovery_label_fraction"]):
            values = part.groupby("k")[metric].agg(["mean", "std"])
            ax.errorbar(values.index, values["mean"], yerr=values["std"], marker="o", label=f"{rep} labels={frac:g}")
        ax.set(xlabel="k", ylabel=metric, xticks=[2, 4, 8])
        ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(figure_dir / "alignment.png", dpi=160)
    plt.close(fig)
    for selection, selected in results.groupby("selection"):
        fractions = sorted(selected.label_fraction.unique())
        # ให้ทั้ง 16 วิธีมีสีต่างกัน และใช้สัญลักษณ์ช่วยอ่านกรณีพิมพ์ขาวดำ
        method_names = sorted(selected.method.unique())
        colors = {name: plt.get_cmap("tab20")(i) for i, name in enumerate(method_names)}
        markers = {name: ["o", "s", "^", "D", "v", "P", "X", "*"][i % 8]
                   for i, name in enumerate(method_names)}
        fig, axes = plt.subplots(1, len(fractions), figsize=(7*len(fractions), 5), squeeze=False)
        for fraction, ax in zip(fractions, axes[0]):
            part = selected[selected.label_fraction == fraction]
            for method, group in part.groupby("method"):
                ax.errorbar(group.eo_gap.mean(), group.accuracy.mean(),
                            xerr=group.eo_gap.std(), yerr=group.accuracy.std(),
                            fmt=markers[method], color=colors[method], label=method)
            ax.set(xlabel="EO gap (lower is better)", ylabel="Accuracy", title=f"Labels {fraction:.0%} / {selection}")
        axes[0, -1].legend(fontsize=7, loc="center left", bbox_to_anchor=(1, 0.5))
        fig.tight_layout()
        fig.savefig(figure_dir / f"accuracy_eo_{selection}.png", dpi=160, bbox_inches="tight")
        plt.close(fig)
        fig, ax = plt.subplots(figsize=(11, 5))
        for method, part in selected.groupby("method"):
            values = part.groupby("label_fraction").worst_group_accuracy.agg(["mean", "std"])
            ax.errorbar(values.index, values["mean"], yerr=values["std"],
                        marker=markers[method], color=colors[method], label=method)
        ax.set(xlabel="Label fraction", ylabel="Worst-group accuracy", title=selection, xticks=fractions)
        ax.legend(fontsize=7, loc="center left", bbox_to_anchor=(1, 0.5))
        fig.tight_layout()
        fig.savefig(figure_dir / f"worst_group_labels_{selection}.png", dpi=160)
        plt.close(fig)
