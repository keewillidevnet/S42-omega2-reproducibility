# S4,2(x): Certified Closed Forms for a Weight-6 Euler Sum

Exact, precision-certified closed forms for the weight-6 Euler sum

    S4,2(x) = sum_{n >= 1} H_{n-1} x^n / n^5,    H_n = sum_{k=1}^n 1/k,

at dyadic arguments, together with a Lean 4 / Mathlib formalization, a high-precision certification protocol, and constant-folded evaluation benchmarks.

This is the corrected revision (v2.0). It supersedes the January 12, 2026 version, whose exact claims at all three dyadic arguments have been withdrawn (see Background).

## Why this matters

S4,2(x) is a weight-6 polylogarithmic object. Constants of this kind appear in analytic number theory and in perturbative physics, where weight-6 polylogarithms turn up in Feynman-integral evaluations. An exact closed form, a finite rational combination of a fixed set of standard constants, is useful in two distinct ways.

Identification and proof. The corrected identity expresses S4,2(1/2) as a rational combination of zeta values, powers of log 2, polylogarithms at 1/2, and one irreducible weight-6 Euler sum. With it in hand you can recognize the value when it appears elsewhere, prove relations against it, and treat it as a known constant rather than an opaque number.

Cheap repeated evaluation. Direct summation needs more terms as you ask for more precision. A closed form does not. Once the basis constants are precomputed, evaluating S4,2 reduces to a fixed-length dot product whose cost does not grow with the number of series terms convergence would have required. When the same value is needed many times at high precision, the one-time basis cost amortizes and the marginal cost approaches a single dot product. This repository includes the crossover analysis and a batched microbenchmark showing order-of-magnitude throughput gains for this family. Numerical exactness is established separately, by high-precision CPU evaluation.

A methodological point underlies all of this: a high-precision numerical match is not an exact identity. The correction described below exists precisely because a relation can agree to a hundred digits and still be wrong. This repo therefore certifies identities by a standard stronger than a single residual (see Certification standard).

## Use cases

- Identifying an unknown high-precision weight-6 constant against a fixed basis.
- Fast, arbitrary-precision, repeated evaluation of S4,2 at dyadic points inside a numerical library.
- A certified reference value for testing other implementations.
- A worked template for vetting PSLQ-discovered identities, where precision tracking separates genuine identities from approximations.
- A starting point for formalizing Euler-sum identities in Lean, where Mathlib currently provides no polylogarithm or Euler-sum infrastructure.

## Corrected status

| Argument | Status | Implemented here |
| --- | --- | --- |
| x = 1/2 | Corrected exact closed form in a 13-element dyadic basis | Yes |
| x = 1/4 | Certified exact relation in a depth-2 MPL basis | Yes |
| x = -1/2 | Open; no certified closed form | No |

The x = 1/4 result is deliberately not described as a reduction to independently known constants, because its right-hand side still contains unreduced depth-2 multiple polylogarithms, including Li_{5,1}(-1/2) = S4,2(-1/2).

## Formalization (Lean 4 / Mathlib)

The x = 1/2 closed form is also formalized in Lean 4, in the `formalization/` directory. This is nontrivial because Mathlib has no polylogarithms, Nielsen polylogarithms, multiple zeta values, or Euler sums. Even stating the identity requires building scaffolding from the harmonic numbers and Riemann zeta values that Mathlib does provide.

Status: the main theorem `S42_half` is machine-checked modulo exactly two functional-equation obligations, on the corrected domain (0, z0] with z0 = (log 2)/2. Everything else it rests on is fully kernel-verified, with axiom dependencies limited to `[propext, Classical.choice, Quot.sound]`:

- `F_zero`: the base case F0(x) = -x log(1 - x) / (1 - x), via a Cauchy product.
- `F_hasDerivAt`, `Li_hasDerivAt`: the differentiation ladder d/dx F_s = F_{s-1} / x, by term-by-term differentiation on a sub-disk.
- `Li_neg_one`: the reduction Li_n(-1) = -(1 - 2^{1-n}) zeta(n).
- `args_at_z0`, `S42_half_conditional`: the argument specializations and the closed form given the functional equation.
- `abel_neg_one`, `Li_tendsto_neg_one`, `F_tendsto_neg_one`, `a_tendsto`, `feLHS_continuousWithinAt_z0`, `feRHS_continuousWithinAt_z0`: Abel boundary continuity, which closes the endpoint z0 by a left-limit rather than assuming it.

The two remaining `sorry`s are `fe_deriv_eq`, the weight-5 functional equation that heads the weight-induction tower, and `fe_basepoint`, its integration constant. `functionalEquation` and `S42_half` are sorry-free in their own bodies and reach `sorryAx` only through those two. An earlier statement carried a false branch over the divergent region (z0, log 2), where the argument 1 - e^{2z} leaves the unit disk; that branch has been removed, so the statement is now restricted to the convergence region and the endpoint z0 is recovered by the boundary-continuity lemmas above. See `formalization/AXIOMS.txt` for the `#print axioms` output and `formalization/README.md` for details.

## Background: the correction

The January 2026 version claimed exact closed forms at all three arguments in a 21-element basis. On re-examination, those coefficients reproduced the values to about 98 digits and then stopped improving as precision rose, which is the signature of a high-precision approximation, not an exact identity. The basis was both contaminated, in that it included level-6 Clausen constants at pi/3 that do not arise from polylogarithms at dyadic arguments, and incomplete, in that it omitted the single irreducible depth-2 generator of the weight-6 level-2 space. The corrected x = 1/2 basis has 13 elements, and its residual tracks precision, falling below 1e-500 at 500-digit precision. The earlier exact claims at all three arguments are withdrawn.

## Certification standard

A relation is accepted only when both hold:

1. the residual decreases as working precision increases, instead of plateauing; and
2. the rational coefficients remain stable across increasing precision levels.

A single small residual at one precision is not treated as certification of exactness.

### Deprecated v1 claims

Do not use any of the following from the January 2026 version:

- exact closed forms at all three dyadic arguments;
- the 21-element basis;
- Clausen constants at pi/3 as part of the dyadic reduction basis;
- residuals near 1e-98 as proof of exactness without precision tracking.

The benchmark and amortized constant-folding discussion remain valid, now tied to the corrected x = 1/2 closed form and the x = 1/4 certified relation.

## Install

    python -m venv .venv
    source .venv/bin/activate
    pip install -e .
    pip install pytest

## Quick verification

    pytest -q

Example:

    from mpmath import mp
    from s42 import evaluate_series, evaluate_relation, get_relation_status

    mp.dps = 80
    for x in (0.5, 0.25):
        series_value = evaluate_series(x)
        relation_value = evaluate_relation(x)
        print(x, get_relation_status(x))
        print(abs(series_value - relation_value))

Evaluating the withdrawn x = -1/2 closed form raises an error, because that case is open.

## Key files

| Path | Purpose |
| --- | --- |
| `src/s42/basis.py` | Corrected 13-element dyadic basis and x=1/4 depth-2 relation basis |
| `src/s42/coefficients.py` | Corrected rational coefficient vectors |
| `src/s42/closed_form.py` | Dot-product evaluator for the corrected closed form and relation |
| `src/s42/series.py` | Direct Euler-sum evaluator for verification |
| `tests/test_corrected_revision.py` | Regression tests for the corrected revision |
| `formalization/` | Lean 4 formalization of the x=1/2 closed form (see its README) |
| `formalization/AXIOMS.txt` | `#print axioms` output for the Lean lemmas |
| `docs/S42_paper.tex` | Corrected manuscript text |

## Citation

See `CITATION.cff`. The reproducibility archive is also deposited on Zenodo at https://doi.org/10.5281/zenodo.18226314.

## License

MIT. See `LICENSE`.
