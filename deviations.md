# Deviations log (plan v2.0 section 4.4)

## 2026-11-21 - Tier C, design A, OH 2024: crash (no result produced)

- Context: tier C opened once (GA, CA, OH 2024 downloaded once into `_C_2026-11/data/hmda/`, schema header check OK for all three). Design A run sequentially GA, CA, OH with the frozen v2.0 code (manifest verified before start; code+config SHA fac250ab...ba99).
- GA 2024 A: rc=0 (2552 s). CA 2024 A: rc=0 (3798 s).
- OH 2024 A: rc=1 after 206 s, in seed 17 at the cluster-score step. Log: `_C_2026-11/A_OH.err.log`.
  - `fairgroups/run.py:190 group_scores(...)` -> `hmda_groups.py:64 silhouette_score(...)` -> sklearn `ValueError: Number of labels is 1. Valid values are 2 to n_samples - 1 (inclusive)`.
  - Meaning: at least one candidate clustering on OH 2024 train data yielded a single label, which sklearn's silhouette rejects. No confirm/ output was written for OH (only data_profile / filter_counts / mlflow.db in `_C_2026-11/A/OH/`).
- Actions taken: chain stopped by design (design B for GA/CA/OH NOT run). No re-download, no rerun, no code edit. No group counts or approval rates were inspected.
- Decision needed from the user before any change: code in the v2.0 manifest cannot be edited without going through the user. Per plan 4.4 the result before and after any fix must both be reported.

## 2026-11-21 22:2x - fix proposed/applied after the A OH crash (first attempt failed)

- Root cause refined: `group_scores` already skips silhouette when the full label vector has < 2 clusters, but `silhouette_score(sample_size=1000)` subsamples 1,000 rows; when one cluster is tiny the sample holds a single label and sklearn raises ValueError. First attempt of A OH 2024 therefore failed (seed 17, 206 s, log `_C_2026-11/A_OH.log`, `A_OH.err.log`, kept).
- Approved by the user ("แก้ตามเสนอ"). Minimal change in `src/fairgroups/hmda_groups.py` (group_scores only): wrap the silhouette call in `try/except ValueError` and set silhouette = NaN; Davies-Bouldin still computed on all rows.
```diff
-        out.update(silhouette=float(silhouette_score(x,labels,sample_size=min(1000,len(labels)),random_state=seed)),
-                   davies_bouldin=float(davies_bouldin_score(x,labels)))
+        try:
+            sil = float(silhouette_score(x,labels,sample_size=min(1000,len(labels)),random_state=seed))
+        except ValueError:   # sampled subset contains a single label (deviation 2026-11-21, see deviations.md)
+            sil = np.nan
+        out.update(silhouette=sil, davies_bouldin=float(davies_bouldin_score(x,labels)))
```
- No effect on numbers whenever sklearn does not raise (GA/CA A and B GA never raised: rc=0), because the try block returns the identical value.
- Caveat: `run.py:201/226` pick k with `max(..., key=silhouette)`; a NaN at the first k would be kept by `max` (comparisons with NaN are False). Not changed (run.py is out of scope); check the OH selection after any rerun.
- Test: `tests/test_group_scores_single_label.py` (fails without the fix with the real sklearn ValueError, passes with it).
- Consequence: `hmda_groups.py` is in manifest v2.0, so `freeze_v2.py --verify` now reports "code/config changed" and the access guard refuses 2024 (checked: AccessDenied for OH 2024). A OH was NOT rerun; waiting for the user to decide (e.g. addendum manifest). Manifest and access_guard untouched.
- Runs completed BEFORE the edit used the frozen code exactly (A GA, A CA, B GA).

## 2026-11-21 22:17 - design B CA blocked by the guard (structural, not transient)

- `design_b.core.run_design_b` first calls `require_access(state, 2023)`. For CA/OH 2023 that is tier R, which verifies manifest **v1.0** against the plan SHA passed in (v2.0 plan) -> "SHA-256 ของแผนไม่ตรงกับ manifest ที่ตรึงไว้" (also v1.0 verify fails by design since v2 changed freeze.py/hmda.py). So B for CA and OH cannot pass the guard with one `--plan-file`; B GA passes because GA 2023 is tier D (no unlock). B CA stopped at 9 s before touching any file (no data read; `_C_2026-11/B_CA.err.log`, status.txt). Not retried, no guard bypass. Needs a user decision.
