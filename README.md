# S42 Omega2 Reproducibility — Corrected Revision

This repository accompanies the corrected revision of:

**Certified Reductions of the Weight-6 Euler Sum at Dyadic Arguments: A Corrected Exact Closed Form at `x = 1/2`, a Certified Relation at `x = 1/4`, and the Boundary of the Dyadic Field**

The corrected revision supersedes the January 12, 2026 version. The original repo claimed exact closed forms for `S_{4,2}(x)` at `x ∈ {1/2, 1/4, -1/2}` in a 21-element Ω₂ basis. That claim has been withdrawn. The old 21-element basis included level-6 Clausen constants and omitted the single irreducible depth-2 generator required by the weight-6 level-2 space.

## Corrected status

| Argument | Revised status | Implemented here |
|---|---|---|
| `x = 1/2` | Corrected exact closed form in a 13-element dyadic basis | Yes |
| `x = 1/4` | Certified exact relation in a depth-2 MPL basis | Yes |
| `x = -1/2` | Open; no certified closed form | No closed-form implementation |

The `x = 1/4` result is intentionally not described as a reduction to independently known constants because its right-hand side contains unreduced depth-2 multiple polylogarithms, including `Li_{5,1}(-1/2) = S_{4,2}(-1/2)`.

## Certification standard

A relation is accepted only when:

1. the residual decreases as working precision increases, instead of plateauing; and
2. the rational coefficients remain stable across increasing precision levels.

A single small residual at one precision is not treated as certification of exactness.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest
```

## Quick verification

```bash
pytest -q
```

Example:

```python
from mpmath import mp
from s42 import evaluate_series, evaluate_relation, get_relation_status

mp.dps = 80
for x in (0.5, 0.25):
    series_value = evaluate_series(x)
    relation_value = evaluate_relation(x)
    print(x, get_relation_status(x))
    print(abs(series_value - relation_value))
```

Attempting to evaluate the withdrawn `x = -1/2` closed form raises an error because that case remains open.

## Key files

| File | Purpose |
|---|---|
| `src/s42/basis.py` | Corrected 13-element dyadic basis and `x=1/4` depth-2 relation basis |
| `src/s42/coefficients.py` | Corrected rational coefficient vectors |
| `src/s42/closed_form.py` | Dot-product evaluator for the corrected closed form/relation |
| `src/s42/series.py` | Direct Euler-sum evaluator for verification |
| `tests/test_corrected_revision.py` | Regression tests matching the corrected revision |
| `docs/S42_paper.tex` | Corrected manuscript text |

## Deprecated v1 claims

The following v1 claims should not be used:

- exact closed forms at all three dyadic arguments;
- the 21-element Ω₂ basis;
- Clausen constants at `π/3` as part of the dyadic reduction basis;
- residuals near `1e-98` as proof of exactness without precision tracking.

The benchmark and amortized constant-folding discussion remain useful, but their interpretation is now tied to the corrected `x=1/2` closed form and the `x=1/4` certified depth-2 relation.
