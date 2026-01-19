# S₄,₂(x) Exact Ω₂ Identities - Reproducible Research Repository

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.18226314-blue?logo=zenodo&logoColor=white)](https://doi.org/10.5281/zenodo.18226314)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Companion repository for:** "Exact Ω₂ Identities for S₄,₂(x) with Amortized Performance Gains" by Keenan Williams (January 2026)

## Overview

This repository provides **exact closed-form identities** for the weight-6 Euler sum:

```
S₄,₂(x) = Σ(n≥1) [H_{n-1} · x^n] / n^5
```

at three rational points **x ∈ {1/2, 1/4, -1/2}**, expressed in a canonical 21-element Ω₂ basis of weight-6 constants.

**Repository features:**
- ✅ **Complete reproducibility**: All paper results with standalone scripts
- ✅ **Modular package**: Installable Python package for extension
- ✅ **Full documentation**: Paper, code, and detailed guides
- ✅ **GPU validation**: Apple MPS benchmarks included
- ✅ **Exact coefficients**: All 63 PSLQ-discovered rationals

## Paper Results

| x value | Series eval (120 dps) | Closed form | Speedup | Absolute error |
|---------|----------------------|-------------|---------|----------------|
| 1/2 | 3.356 ms | 155.6 μs | 21.6× | 2.7×10⁻⁹⁸ |
| 1/4 | 1.873 ms | 152.5 μs | 12.3× | 2.9×10⁻⁹⁸ |
| -1/2 | 3.368 ms | 159.2 μs | 21.2× | 1.3×10⁻⁹⁹ |

**GPU (PyTorch MPS):** 39×-241× speedup for batch evaluation (float32)

---

## Quick Start

This repository supports two workflows:

### 🔬 For Reviewers: Reproduce Paper Results

**Use the standalone scripts (exact paper reproduction):**

```bash
# Clone and setup
git clone https://github.com/keewillidevnet/S42-omega2-reproducibility.git
cd S42-omega2-reproducibility
python -m venv s42env
source s42env/bin/activate  # Windows: s42env\Scripts\activate
pip install -r requirements.txt

# Reproduce Table 1 (CPU benchmarks at 120 dps)
python scripts/benchmark_fully_folded.py

# Reproduce Figure 1a (Speedup vs Precision)
python scripts/S42_speedup_plot.py
# Output: results/figures/S42_speedup_vs_precision.png

# Reproduce Figure 1b (Error vs Precision)
python scripts/S42_error_plot.py
# Output: results/figures/S42_error_vs_precision.png

# Reproduce Table 2 (GPU benchmarks, requires PyTorch)
python scripts/benchmark_gpu.py
```

**That's it!** These scripts are self-contained and match the paper exactly.

### 🔧 For Developers: Extend the Work

**Use the modular package:**

```bash
# Install as package
pip install -e .

# Use the API
python
>>> from s42 import evaluate_closed_form, evaluate_series
>>> from mpmath import mp
>>> 
>>> mp.dps = 100
>>> value = evaluate_closed_form(x=0.5)
>>> print(value)  # High-precision result
>>> 
>>> # Compare methods
>>> series_val = evaluate_series(x=0.5, precision=100)
>>> closed_val = evaluate_closed_form(x=0.5, precision=100)
>>> print(f"Error: {abs(series_val - closed_val)}")

# Run extended benchmarks
python scripts/benchmark_cpu.py --precision 160 --target all

# View coefficients
python -c "from s42 import print_coefficients; print_coefficients(0.5)"
```

---

## Repository Structure

```
S42-omega2-reproducibility/
├── Paper & Documentation
│   ├── docs/S42_paper.pdf              # Published paper
│   ├── docs/S42_paper.tex              # LaTeX source
│   ├── CITATION.cff                    # Citation metadata
│   ├── README.md                       # This file
│   ├── INTEGRATION_GUIDE.md            # Dual structure explained
│   └── STRUCTURE.md                    # Detailed organization
│
├── Reproduction Scripts (Standalone)
│   ├── scripts/benchmark_fully_folded.py   # Table 1 (CPU)
│   ├── scripts/benchmark_gpu.py            # Table 2 (GPU)
│   ├── scripts/S42_speedup_plot.py         # Figure 1a
│   ├── scripts/S42_error_plot.py           # Figure 1b
│   ├── scripts/benchmark_original.py       # Basic benchmark
│   └── scripts/benchmark_folded.py         # Folded benchmark
│
├── Modular Package (Development)
│   └── src/s42/
│       ├── __init__.py         # Public API
│       ├── basis.py            # Ω₂ basis computation (21 elements)
│       ├── coefficients.py     # All 63 exact coefficients
│       ├── series.py           # Series evaluation
│       ├── closed_form.py      # Closed-form evaluation
│       ├── pslq.py             # PSLQ verification
│       └── utils.py            # Helper functions
│
├── Extended Features
│   ├── scripts/benchmark_cpu.py        # Modular CPU benchmark
│   ├── scripts/quick_start.py          # Getting started example
│   └── scripts/verify_pslq.py          # Verify coefficients
│
├── Results
│   └── results/figures/
│       ├── S42_speedup_vs_precision.png   # Figure 1a
│       └── S42_error_vs_precision.png     # Figure 1b
│
└── Configuration
    ├── setup.py                # Package installation
    ├── requirements.txt        # Dependencies
    ├── environment.yml         # Conda alternative
    └── LICENSE                 # MIT License
```

---

## Mathematical Details

### The Euler Sum

```
S₄,₂(x) = Σ(n=1 to ∞) [H_{n-1} · x^n] / n^5

where H_n = Σ(k=1 to n) 1/k  (harmonic numbers)
```

This is a weight-6 Euler sum (harmonic weight 4 + power weight 2).

### Ω₂ Basis (21 elements, weight-6)

The canonical basis consists of:

1. **Zeta values:** ζ(6), ζ(3)²
2. **Mixed zeta-log:** ζ(5)log2, ζ(3)log³2
3. **Pi-log products:** π⁴log²2, π²log⁴2, log⁶2
4. **Polylogarithms:** Li₆(1/2), Li₆(1/4), Li₅(1/2)log2, Li₅(1/4)log2, Li₄(1/2)log²2, Li₄(1/4)log²2
5. **Mixed poly-pi:** π²Li₄(1/2), π²Li₄(1/4)
6. **Clausen values:** Cl₆(π/3), π²Cl₄(π/3), π⁴Cl₂(π/3), π²Cl₂(π/3)², Cl₂(π/3)³
7. **Constant:** 1

### Exact Identities

**x = 1/2:**
```
S₄,₂(1/2) = (15683/14280)ζ(6) + (-5743/14280)ζ(3)² + ... [21 terms total]
```

See `src/s42/coefficients.py` or paper Appendix A for complete formulas.

All coefficients are **exact rationals** discovered via PSLQ with residuals < 10⁻⁹⁶.

---

## Usage Examples

### Example 1: Basic Evaluation

```python
from s42 import evaluate_closed_form
from mpmath import mp

mp.dps = 50  # 50 decimal places
value = evaluate_closed_form(x=0.5)
print(value)
```

### Example 2: Compare Series vs Closed Form

```python
from s42 import evaluate_series, evaluate_closed_form
from mpmath import mp

mp.dps = 100

# Evaluate both ways
series_val = evaluate_series(x=0.5)
closed_val = evaluate_closed_form(x=0.5)

# Check agreement
error = abs(series_val - closed_val)
print(f"Absolute error: {error}")  # Should be ~10⁻⁹⁸
```

### Example 3: View Coefficients

```python
from s42 import get_coefficients, print_coefficients

# Get as fractions
coeffs = get_coefficients(0.5)
print(f"First coefficient: {coeffs[0]}")  # 15683/14280

# Pretty print
print_coefficients(0.5, format_type="fraction")
```

### Example 4: Verify PSLQ

```python
from s42 import verify_pslq_identity

# Verify at high precision
residual, coeffs = verify_pslq_identity(
    x=0.5,
    precision=200,
    verbose=True
)
# Should print: Residual < 10⁻⁹⁶
```

### Example 5: Batch Evaluation

```python
from s42 import batch_evaluate_closed_form

values = batch_evaluate_closed_form(
    x_values=[0.5, 0.25, -0.5],
    precision=100
)
# Basis computed once, reused for all three
```

---

## Performance Analysis

### Amortized Cost Model

For N evaluations at precision p:

```
Total cost:
  Series:      N × T_series(p)
  Closed form: T_basis(p) + N × T_dot(p)

Crossover: N* = T_basis(p) / [T_series(p) - T_dot(p)]
```

**Typical crossover:** ~20-30 evaluations (depends on precision)

### When to Use Each Method

**Use series when:**
- Single one-off evaluation
- Arbitrary x values (not just {1/2, 1/4, -1/2})
- N < N* evaluations

**Use closed form when:**
- Multiple evaluations (N > N*)
- Batch processing on GPU/TPU
- Need consistent performance across precisions

---

## Installation

### Option 1: User (pip)

```bash
pip install git+https://github.com/keewillidevnet/S42-omega2-reproducibility.git
```

### Option 2: Developer (editable)

```bash
git clone https://github.com/keewillidevnet/S42-omega2-reproducibility.git
cd S42-omega2-reproducibility
pip install -e .
```

### Option 3: Conda

```bash
conda env create -f environment.yml
conda activate s42env
pip install -e .
```

### Dependencies

**Required:**
- mpmath ≥ 1.3.0 (arbitrary precision)
- numpy ≥ 1.24.0

**Optional:**
- matplotlib ≥ 3.7.0 (for plots)
- sympy ≥ 1.12 (for symbolic verification)
- torch ≥ 2.0.0 (for GPU benchmarks)
- pytest ≥ 7.4.0 (for testing)

---

## Testing

```bash
# Run test suite (when tests are written)
pytest tests/ -v

# With coverage
pytest tests/ --cov=src/s42 --cov-report=html
```

---

## Citation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18226314.svg)](https://doi.org/10.5281/zenodo.18226314)

If you use this work in your research, please cite:

Keenan Williams. (2026). *S42-omega2-reproducibility* (Version 1.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.18226314

**BibTeX:**
```bibtex
@software{williams2026s42,
  author    = {Williams, Keenan},
  title     = {S42-omega2-reproducibility},
  year      = {2026},
  publisher = {Zenodo},
  version   = {1.0},
  doi       = {10.5281/zenodo.18226314},
  url       = {https://doi.org/10.5281/zenodo.18226314}
}
```

---

## Contributing

Contributions welcome! Areas of interest:
- New x values (e.g., x = 1/3, 1/8)
- Other weight-6 Euler sums (S₃,₃, S₅,₁)
- GPU optimization (CUDA support)
- Symbolic verification

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Documentation

- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)**: Explains dual structure (reproduction + development)
- **[STRUCTURE.md](STRUCTURE.md)**: Detailed repository organization
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: How to contribute
- **[docs/S42_paper.pdf](docs/S42_paper.pdf)**: The research paper
- **[docs/MATHEMATICAL_DETAILS.md](docs/MATHEMATICAL_DETAILS.md)**: Math background (to be written)
- **[docs/API.md](docs/API.md)**: API documentation (to be written)

---

## Reproducibility Checklist

For reviewers:

- ✅ **Platform**: macOS (Apple Silicon), Python 3.13.5
- ✅ **Environment**: `s42env` virtual environment
- ✅ **Libraries**: mpmath (required), torch (optional for GPU)
- ✅ **Scripts**: All in `scripts/` directory
- ✅ **Data**: Figures in `results/figures/`
- ✅ **Paper**: `docs/S42_paper.pdf`
- ✅ **Coefficients**: Embedded in scripts and `src/s42/coefficients.py`
- ✅ **PSLQ residuals**: < 10⁻⁹⁶ (verified in scripts)

**To reproduce Table 1:** `python scripts/benchmark_fully_folded.py`  
**To reproduce Figure 1:** `python scripts/S42_speedup_plot.py && python scripts/S42_error_plot.py`  
**To reproduce Table 2:** `python scripts/benchmark_gpu.py` (requires PyTorch)

---

## License

MIT License - see [LICENSE](LICENSE) file

---

## Contact

**Keenan Williams**  
Email: telesis001@icloud.com  

---

## Acknowledgments

- PSLQ algorithm by Bailey & Ferguson
- mpmath library by Fredrik Johansson
- Inspired by work of Borwein, Bailey, and collaborators on Euler sums

---
