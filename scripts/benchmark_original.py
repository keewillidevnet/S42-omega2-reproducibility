#!/usr/bin/env python3
"""Deprecated v1 benchmark guard.

The original benchmark used the withdrawn 21-element Omega2 basis with Clausen
constants. It is intentionally disabled so stale v1 claims cannot be reproduced
as if they were corrected results.
"""
raise SystemExit(
    "Deprecated: the v1 21-element Omega2/Clausen benchmark is withdrawn. "
    "Use scripts/benchmark_cpu.py or scripts/benchmark_folded.py instead."
)
