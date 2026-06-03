# Repository Structure

This repository implements the corrected S_{4,2}(x) revision.

## Core package

```text
src/s42/
  basis.py          corrected 13-element dyadic basis and x=1/4 depth-2 relation basis
  coefficients.py   certified coefficient vectors for x=1/2 and x=1/4
  closed_form.py    relation evaluators; exact terminology applies only to x=1/2
  series.py         direct series evaluator
  pslq.py           integer-relation and residual-tracking utilities
```

## Scripts

```text
scripts/quick_start.py              smoke test for corrected claims
scripts/benchmark_cpu.py            CPU timing of direct series vs corrected relation
scripts/benchmark_folded.py         constant-folded timing for corrected relations
scripts/benchmark_fully_folded.py   alias for benchmark_folded.py
scripts/benchmark_gpu.py            optional GPU benchmark for corrected x=1/2 vector
scripts/benchmark_original.py       deprecated-v1 guard; prints why old basis is invalid
scripts/S42_error_plot.py           corrected residual-tracking figure generator
scripts/S42_speedup_plot.py         corrected speedup figure generator
```

## Corrected mathematical status

| Argument | Implemented status |
|---|---|
| `1/2` | exact closed form in the corrected 13-element dyadic basis |
| `1/4` | certified exact depth-2 MPL relation, not a reduction to known constants |
| `-1/2` | open; no closed form is implemented |

The withdrawn v1 21-element Omega2 basis and Clausen-at-pi/3 constants are not part of the corrected implementation.
