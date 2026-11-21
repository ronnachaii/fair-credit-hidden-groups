"""Design B (plan section 4.5): transfer the 2023 models/groups/thresholds to 2024 without refitting.

This package lives in a sub-directory on purpose: tools/freeze_v1.py hashes only src/fairgroups/*.py (non-recursive),
so adding it does not change the v1.0 manifest. It is NOT covered by the v1.0 hash -- it must be added to the v2.0
freeze before the 2024 data is opened.
"""
from .core import (SchemaMismatch, SourceModel, fit_source, apply_source, build_transfer_inputs,
                   run_design_b_arrays, run_design_b)

__all__ = ["SchemaMismatch", "SourceModel", "fit_source", "apply_source", "build_transfer_inputs",
           "run_design_b_arrays", "run_design_b"]
