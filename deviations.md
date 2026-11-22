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

## 2026-11-22 - access guard / freeze changed (addendum v2.1) so the fixed code can open C again

- Why: after the `hmda_groups.py` fix (above) manifest v2.0 no longer matched the code, so the guard refused A OH 2024. Also design B re-reads CA/OH **2023** (tier R), which the guard verified against manifest v1.0 with the v2.0 plan SHA, so B CA was refused structurally (B GA passed because GA 2023 is tier D). User approved an addendum ("ทำตามเสนอ").
- `freeze/v2_1_manifest.json` (new; `v2_0_manifest.json` untouched, sha256 9e454bdf...fd21fb): same plan SHA 2e422e2a...0329a, current hashes of the 72 files, reference to the v2.0 manifest file hash, and a `changes` block with before/after hashes and a reason for each of the 4 changed files: `src/fairgroups/hmda_groups.py`, `src/fairgroups/freeze.py`, `src/fairgroups/access_guard.py`, `tools/freeze_v2.py`. v2.1 code+config SHA cd44e13e...acc43e. Written with `python tools/freeze_v2.py --write-addendum`.
- `freeze.py`: tier v2.1 uses the v2.0 file list; `verify_manifest` additionally checks an addendum (base manifest hash unchanged, same plan SHA, every file that differs from the base is listed with matching hashes and a reason).
- `access_guard.py` (only `require_access` body): tier C verifies manifest v2.1 first, then v2.0. Tier R is additionally accepted when BOTH `--unlock-R` and `--unlock-C` equal the v2.0 plan SHA (also equal to the plan file's SHA) and manifest v2.1 verifies; otherwise the original v1.0 path applies unchanged. Still required: unlock flags, plan file SHA, code/config hash match, library versions, open_log entry on every open; unlisted states/years still refused. Note: the guard never verified data-file hashes before and still does not (the 2023/2024 file SHAs are recorded in `freeze/R_data_manifest.json` and `freeze/C_data_manifest.json`).
- `tools/freeze_v2.py`: `--addendum`, `--write-addendum`, `--tier`.
- Tests: `tests/test_freeze_addendum.py` (pass cases and blocked cases: wrong plan SHA, no unlock, unlocks disagree, missing reason, edited base manifest, code drift after v2.1, unlisted state).
- Runs completed before the edits (A GA, A CA, B GA) used the v2.0-frozen code unchanged.

## 2026-11-22 - reruns under addendum v2.1 (guard passed; code+config SHA cd44e13e...acc43e)

- A OH 2024 rerun (first attempt failed, kept as `_C_2026-11/A/OH_failed_attempt1/` + `A_OH.log`/`A_OH.err.log`): rc=0, 2121 s, output `_C_2026-11/A/OH/`, log `A_OH_retry.log`.
- B CA (retry of the 9-second guard refusal; `B_CA.log` kept): rc=0, 1552 s. B OH: rc=0, 834 s. Outputs `_C_2026-11/B/<ST>/design_B/`.
- Silhouette NaN in A OH: 5 of 100 rows in `A/OH/clustering_results.csv` (scarf, definition c, k=2, all five seeds 17/29/43/59/71); GA and CA have 0 NaN. Confirmatory table uses fixed k_main=8 (confirmatory.py), so it does not use the silhouette-based k selection; `run.py` k selection and `proposed_selected` in postprocess_results.csv do (see report).

## 2026-11-22 - plan/code mismatch noted (not a post-C fix): H3b uses the CI lower bound of delta-accuracy

- Plan v2.0 clarification P4 (V1): the delta-accuracy criterion >= -0.02 uses the POINT estimate. Code frozen in manifest v2.0/v2.1 (`src/fairgroups/confirmatory.py`, `_hypotheses`):
  - line ~297: `H3b` passes_state = `lower(B_rand) > m and lower(B_single) > m and lower(dAcc_method) > da` -> the delta-acc part uses the one-sided 95% LOWER bound (p_state uses `p_greater(dAcc_method, da)` from the bootstrap).
  - line ~308 `flag_benefit_appears` uses the point value (`point["dAcc_method"][0] >= da`), consistent with P4.
  - So P4 holds for the flag but not for the H3b test. Code NOT changed (frozen; this is a mismatch present since v1.0/R, not introduced after opening C).
- Re-check from result files (`confirm_bootstrap_summary_{row,lei}.csv`, m = 0.01, da = -0.02; "point" variant = lower(B_rand) > m, lower(B_single) > m, point dAcc >= da):

| set | boot | lower B_rand | lower B_single | dAcc point | dAcc lower | H3b (lower, as run) | H3b (point variant) |
|---|---|---|---|---|---|---|---|
| C A GA | row | 0.0147 | 0.0163 | -0.0187 | -0.0205 | fail | **pass** |
| C A GA | lei | -0.0106 | -0.0096 | -0.0187 | -0.0236 | fail | fail |
| C A CA | row | 0.0044 | -0.0009 | -0.0144 | -0.0155 | fail | fail |
| C A CA | lei | 0.0009 | -0.0027 | -0.0144 | -0.0268 | fail | fail |
| C A OH | row | -0.0397 | -0.0217 | -0.0187 | -0.0203 | fail | fail |
| C A OH | lei | -0.0441 | -0.0226 | -0.0187 | -0.0226 | fail | fail |
| R CA | row | 0.0073 | -0.0057 | -0.0161 | -0.0173 | fail | fail |
| R CA | lei | 0.0036 | -0.0090 | -0.0161 | -0.0336 | fail | fail |
| R OH | row | -0.0236 | -0.0222 | -0.0218 | -0.0235 | fail | fail |
| R OH | lei | -0.0275 | -0.0266 | -0.0218 | -0.0338 | fail | fail |

- Result of the re-check: with the point variant the only per-state-bootstrap cell that changes is C A GA / row (fail -> pass). The state-level decision uses the conservative (max) of row and lei, and GA lei still fails (B conditions not met), so GA stays "fail"; CA and OH fail in both bootstraps because the B_rand/B_single conditions fail, independent of the dAcc rule. Hence the final H3b outcome is unchanged (not passed in any state, so not passed overall), in C and in R (R CA/OH all fail on the B conditions; R dAcc points CA -0.0161, OH -0.0218 as in P4). Caveat: GA row-only would flip, and the p-values (`p_state`) are still those of the lower-bound test.
