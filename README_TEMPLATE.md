# S₄,₂(x) Exact Ω₂ Identities with Amortized Performance Gains

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://img.shields.io/badge/DOI-10.XXXX%2FXXXXXX-blue)](https://doi.org/10.XXXX/XXXXXX)

> **Companion repository for:** "Exact Ω₂ Identities for S₄,₂(x) with Amortized Performance Gains" by Keenan Williams (January 2026)

## Overview

This repository provides complete reproducible code for discovering and evaluating exact closed-form identities for the weight-6 Euler sum:

```
S₄,₂(x) = Σ(n≥1) [H_{n-1} · x^n] / n^5
```

We provide three exact identities at rational points x ∈ {1/2, 1/4, -1/2} expressed in a canonical 21-element Ω₂ basis of weight-6 constants.

## Key Results

| x value | Series eval (120 dps) | Closed form | Per-eval speedup | Absolute error |
|---------|----------------------|-------------|------------------|----------------|
| 1/2 | 3.356 ms | 155.6 μs | 21.6× | 2.7×10⁻⁹⁸ |
| 1/4 | 1.873 ms | 152.5 μs | 12.3× | 2.9×10⁻⁹⁸ |
| -1/2 | 3.368 ms | 159.2 μs | 21.2× | 1.3×10⁻⁹⁹ |

**GPU Acceleration (PyTorch MPS):** 39×-241× speedup for batch evaluation (float32)

## Quick Start

### Option 1: Reproduce Paper Results (Original Scripts)

**For exact paper reproduction:**

```bash
# Clone repository
git clone https://github.com/keewillidevnet/S42-omega2-reproducibility.git
cd S42-omega2-reproducibility

# Set up environment
python -m venv s42env
source s42env/bin/activate  # On Windows: s42env\Scripts\activate
pip install -r requirements.txt

# Run original benchmarks (as in paper)
python scripts/benchmark_fully_folded.py     # Table 1
python scripts/S42_error_plot.py             # Figure 1b
python scripts/S42_speedup_plot.py           # Figure 1a
python scripts/benchmark_gpu.py              # Table 2 (requires PyTorch MPS/CUDA)
```

### Option 2: Use Modular Package (Development)

**For extending the work:**

```bash
# Install package
pip install -e .

# Use the API
python
>>> from s42 import evaluate_series, evaluate_closed_form
>>> from mpmath import mp
>>> mp.dps = 100
>>> value = evaluate_closed_form(x=0.5)
>>> print(value)

# Run new modular benchmarks
python scripts/benchmark_cpu.py --precision 120 --target all
```

## Repository Structure

```
S42-omega2-reproducibility/
├── README.md                   # This file
├── LICENSE                     # MIT License
├── requirements.txt            # Python dependencies
├── environment.yml             # Conda environment (alternative)
├── setup.py                    # Package installation
│
├── src/                        # Source code
│   └── s42/
│       ├── __init__.py
│       ├── basis.py            # Ω₂ basis computation
│       ├── coefficients.py     # Exact rational coefficients
│       ├── series.py           # Series evaluation
│       ├── closed_form.py      # Closed-form evaluation
│       ├── pslq.py             # PSLQ relation finding
│       └── utils.py            # Helper functions
│
├── scripts/                    # Executable scripts
│   ├── benchmark_cpu.py        # CPU benchmarks (Table 1)
│   ├── benchmark_gpu.py        # GPU benchmarks (Table 2)
│   ├── verify_pslq.py          # Verify PSLQ coefficients
│   ├── convergence_study.py    # Series convergence analysis
│   └── generate_figures.py     # Reproduce paper figures
│
├── notebooks/                  # Jupyter notebooks
│   ├── 01_introduction.ipynb   # Getting started
│   ├── 02_basis_exploration.ipynb
│   ├── 03_pslq_discovery.ipynb
│   ├── 04_benchmarks.ipynb
│   └── 05_gpu_validation.ipynb
│
├── tests/                      # Unit tests
│   ├── __init__.py
│   ├── test_basis.py
│   ├── test_coefficients.py
│   ├── test_series.py
│   └── test_closed_form.py
│
├── data/                       # Data files
│   ├── coefficients/           # Exact rational coefficients
│   │   ├── s42_half.json
│   │   ├── s42_quarter.json
│   │   └── s42_neg_half.json
│   └── basis/                  # Pre-computed basis values
│       └── omega2_basis_200dps.json
│
├── results/                    # Benchmark results
│   ├── benchmarks/
│   │   ├── cpu_precision_scaling.csv
│   │   └── gpu_batch_scaling.csv
│   └── figures/
│       ├── speedup_vs_precision.png
│       └── accuracy_vs_precision.png
│
└── docs/                       # Documentation
    ├── paper.pdf               # The paper itself
    ├── MATHEMATICAL_DETAILS.md # Detailed math derivations
    ├── COMPUTATIONAL_NOTES.md  # Implementation details
    └── API.md                  # API documentation
```

## Installation

### Option 1: pip (recommended)

```bash
python -m venv s42env
source s42env/bin/activate
pip install -r requirements.txt
pip install -e .  # Install package in development mode
```

### Option 2: conda

```bash
conda env create -f environment.yml
conda activate s42env
pip install -e .
```

### Dependencies

- Python 3.13+
- mpmath >= 1.3.0 (arbitrary precision arithmetic)
- numpy >= 1.24.0
- scipy >= 1.11.0
- matplotlib >= 3.7.0
- sympy >= 1.12 (optional, for symbolic verification)
- torch >= 2.0.0 (optional, for GPU benchmarks)
- pytest >= 7.4.0 (for testing)

## Usage

### Basic Evaluation

```python
from s42 import evaluate_series, evaluate_closed_form
from mpmath import mp

# Set precision
mp.dps = 120

# Evaluate using series
value_series = evaluate_series(x=0.5, max_terms=600000)

# Evaluate using closed form (faster after basis computation)
value_closed = evaluate_closed_form(x=0.5)

# Check agreement
print(f"Absolute error: {abs(value_series - value_closed)}")
```

### PSLQ Verification

```python
from s42 import verify_pslq_identity
from mpmath import mp

mp.dps = 200

# Verify the identity for x = 1/2
residual, coeffs = verify_pslq_identity(x=0.5)
print(f"PSLQ residual: {residual}")  # Should be < 10^-96
```

### Benchmarking

```python
from s42.benchmarks import benchmark_comparison

# Compare series vs closed form at different precisions
results = benchmark_comparison(
    targets=[0.5, 0.25, -0.5],
    precisions=[50, 80, 120, 160],
    num_evaluations=100
)
```

## Reproducing Paper Results

### Table 1: CPU Benchmarks (120 decimal places)

```bash
python scripts/benchmark_cpu.py \
    --precision 120 \
    --target all \
    --num-trials 100 \
    --output results/benchmarks/table1.csv
```

### Table 2: GPU Benchmarks (float32, MPS backend)

```bash
python scripts/benchmark_gpu.py \
    --backend mps \
    --batch-sizes 1024 2048 4096 8192 16384 32768 65536 131072 \
    --num-trials 50 \
    --output results/benchmarks/table2.csv
```

### Figure 1: Speedup and Accuracy vs Precision

```bash
python scripts/generate_figures.py \
    --figure speedup_vs_precision \
    --output results/figures/fig1a.png

python scripts/generate_figures.py \
    --figure accuracy_vs_precision \
    --output results/figures/fig1b.png
```

## Mathematical Details

### The Euler Sum S₄,₂(x)

```
S₄,₂(x) = Σ(n=1 to ∞) [H_{n-1} · x^n] / n^5

where H_n = Σ(k=1 to n) 1/k
```

This is a weight-6 Euler sum (harmonic weight 4 + power weight 2).

### Ω₂ Basis (21 elements)

The canonical weight-6 basis consists of:

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
S₄,₂(1/2) = (15683/14280)ζ(6) + (-5743/14280)ζ(3)² + ... [21 terms]
```

See `data/coefficients/s42_half.json` for complete coefficients.

**x = 1/4:**
```
S₄,₂(1/4) = (6037/23939)ζ(6) + (540/23939)ζ(3)² + ... [21 terms]
```

**x = -1/2:**
```
S₄,₂(-1/2) = (2879/58060)ζ(6) + (139667/116120)ζ(3)² + ... [21 terms]
```

### PSLQ Discovery

Coefficients were discovered using the PSLQ algorithm:
- Working precision: 200+ decimal digits
- Residual threshold: |r| < 10⁻⁹⁶
- All coefficients are exact rationals

## Performance Analysis

### Amortized Cost Model

For N evaluations at precision p:

```
Total cost (series): N × T_series(p)
Total cost (closed): T_basis(p) + N × T_dot(p)

Crossover: N* = T_basis(p) / [T_series(p) - T_dot(p)]
```

### Typical Crossover Points

| Precision | T_series | T_dot | Est. N* |
|-----------|----------|-------|---------|
| 50 dps | ~1.2 ms | ~80 μs | ~15-20 |
| 80 dps | ~2.1 ms | ~120 μs | ~20-25 |
| 120 dps | ~3.3 ms | ~155 μs | ~25-30 |
| 160 dps | ~5.5 ms | ~190 μs | ~30-35 |

**Interpretation:** Closed form becomes advantageous after ~20-30 repeated evaluations.

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=src/s42 --cov-report=html
```

## Citation

If you use this code in your research, please cite:

```bibtex
@article{williams2026s42,
  title={Exact $\Omega_2$ Identities for $S_{4,2}(x)$ with Amortized Performance Gains},
  author={Williams, Keenan},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2026}
}
```

## License

MIT License - see LICENSE file for details

## Contact

- **Author:** Keenan Williams
- **Email:** [your-email]
- **GitHub:** [@keewillidevnet](https://github.com/keewillidevnet)

## Acknowledgments

- PSLQ algorithm by Bailey & Ferguson
- mpmath library by Fredrik Johansson
- Inspired by the work of Borwein, Bailey, and collaborators on Euler sums

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

See CONTRIBUTING.md for details.

## Changelog

### v1.0.0 (January 2026)
- Initial release
- Three exact identities at x ∈ {1/2, 1/4, -1/2}
- CPU and GPU benchmarks
- Complete PSLQ verification

## Future Work

- [ ] Extend to x = 1/3, 2/3, 1/8, 1/16
- [ ] Other weight-6 Euler sums (S₃,₃, S₅,₁)
- [ ] Symbolic derivation (beyond PSLQ)
- [ ] CUDA backend for GPU benchmarks
- [ ] Automated basis construction
- [ ] Integration with SymPy

## References

1. Bailey, D. H., & Borwein, J. M. (2005). Experimental mathematics: examples, methods and implications. *Notices of the AMS*, 52(5), 502-514.
2. Borwein, J. M., Bradley, D. M., Broadhurst, D. J., & Lisoněk, P. (2001). Special values of multiple polylogarithms. *Transactions of the AMS*, 353(3), 907-941.
3. Ferguson, H. R., & Bailey, D. H. (1992). A polynomial time, numerically stable integer relation algorithm. *RNR Technical Report*, RNR-91-032.

---

**Last updated:** January 11, 2026
