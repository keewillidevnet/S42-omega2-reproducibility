# Repository Structure

This document explains the organization of the S₄,₂ Euler Sum repository.

## Overview

```
S42-omega2-reproducibility/
├── Configuration Files
│   ├── README.md              # Main documentation
│   ├── LICENSE                # MIT License
│   ├── setup.py               # Package installation
│   ├── requirements.txt       # Python dependencies
│   ├── environment.yml        # Conda environment
│   ├── .gitignore            # Git ignore rules
│   └── CONTRIBUTING.md        # Contribution guidelines
│
├── Source Code (src/s42/)
│   ├── __init__.py           # Package initialization
│   ├── basis.py              # Ω₂ basis computation
│   ├── coefficients.py       # Exact rational coefficients
│   ├── series.py             # Series evaluation
│   ├── closed_form.py        # Closed-form evaluation
│   ├── pslq.py               # PSLQ verification
│   └── utils.py              # Utility functions
│
├── Executable Scripts (scripts/)
│   ├── benchmark_cpu.py      # CPU performance benchmarks
│   ├── benchmark_gpu.py      # GPU/TPU benchmarks
│   ├── verify_pslq.py        # PSLQ verification
│   ├── convergence_study.py  # Series convergence analysis
│   ├── generate_figures.py   # Reproduce paper figures
│   └── quick_start.py        # Getting started example
│
├── Notebooks (notebooks/)
│   ├── 01_introduction.ipynb        # Quick start guide
│   ├── 02_basis_exploration.ipynb   # Explore Ω₂ basis
│   ├── 03_pslq_discovery.ipynb      # PSLQ methodology
│   ├── 04_benchmarks.ipynb          # Performance analysis
│   └── 05_gpu_validation.ipynb      # GPU acceleration
│
├── Data Files (data/)
│   ├── coefficients/          # JSON files with exact coefficients
│   │   ├── s42_half.json
│   │   ├── s42_quarter.json
│   │   └── s42_neg_half.json
│   └── basis/                 # Pre-computed basis values
│       └── omega2_basis_200dps.json
│
├── Test Suite (tests/)
│   ├── test_basis.py         # Test basis computation
│   ├── test_coefficients.py  # Test coefficient loading
│   ├── test_series.py        # Test series evaluation
│   └── test_closed_form.py   # Test closed-form evaluation
│
├── Results (results/)
│   ├── benchmarks/           # Benchmark CSV files
│   └── figures/              # Generated plots
│
└── Documentation (docs/)
    ├── paper.pdf             # The research paper
    ├── MATHEMATICAL_DETAILS.md
    ├── COMPUTATIONAL_NOTES.md
    └── API.md                # API documentation
```

## Key Components

### Source Code (`src/s42/`)

#### `basis.py`
- Computes the 21-element Ω₂ weight-6 basis
- Functions:
  - `compute_omega2_basis()`: Compute basis at specified precision
  - `clausen()`: Clausen function evaluation
  - `verify_weight_6()`: Verify dimensional consistency
  - `estimate_basis_computation_time()`: Performance estimation

#### `coefficients.py`
- Stores exact rational coefficients from PSLQ
- Functions:
  - `get_coefficients()`: Retrieve coefficients for x value
  - `print_coefficients()`: Pretty-print with basis names
  - `analyze_coefficient_patterns()`: Statistical analysis

#### `series.py`
- Direct series evaluation of S₄,₂(x)
- Functions:
  - `S42_series()`: Core series summation
  - `evaluate_series()`: Convenience wrapper
  - `estimate_terms_needed()`: Convergence estimation
  - `analyze_convergence()`: Convergence properties
  - `plot_convergence()`: Visualization

#### `closed_form.py`
- Evaluation via exact Ω₂ identities
- Functions:
  - `S42_closed_form()`: Core closed-form evaluation
  - `evaluate_closed_form()`: Convenience wrapper
  - `batch_evaluate_closed_form()`: Multiple x values
  - `compare_with_series()`: Accuracy verification
  - `compute_crossover_point()`: Amortization analysis

#### `pslq.py`
- PSLQ relation finding and verification
- Functions:
  - `verify_pslq_identity()`: Check residual < 10⁻⁹⁶
  - `find_pslq_relation()`: Discover new relations
  - `analyze_pslq_stability()`: Multi-precision verification

#### `utils.py`
- Helper functions
- Includes: harmonic numbers, convergence checking, timing, I/O

### Scripts (`scripts/`)

All scripts support `--help` for usage information.

#### `benchmark_cpu.py`
```bash
# Reproduce Table 1
python scripts/benchmark_cpu.py --precision 120 --target all

# Precision scaling study
python scripts/benchmark_cpu.py --precision-scaling \
    --scaling-precisions 50,80,120,160
```

#### `quick_start.py`
```bash
# Quick demonstration
python scripts/quick_start.py
```

### Notebooks (`notebooks/`)

Interactive tutorials covering:
1. Basic usage and evaluation
2. Exploring the Ω₂ basis structure
3. PSLQ methodology and discovery
4. Performance benchmarking
5. GPU/TPU acceleration

### Data Files (`data/`)

#### Coefficient Files (`data/coefficients/`)
JSON format with exact rational coefficients:
```json
{
  "x_value": "1/2",
  "coefficients": [
    {"numerator": 15683, "denominator": 14280},
    ...
  ],
  "pslq_residual": "2.7e-98",
  "precision": 200
}
```

### Tests (`tests/`)

Test suite using pytest:
```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src/s42 --cov-report=html

# Specific module
pytest tests/test_basis.py -v
```

## Typical Workflows

### 1. Basic Evaluation

```python
from s42 import evaluate_closed_form
from mpmath import mp

mp.dps = 100
value = evaluate_closed_form(x=0.5)
```

### 2. Benchmarking

```bash
python scripts/benchmark_cpu.py \
    --precision 120 \
    --target all \
    --trials 100 \
    --output results/benchmarks/my_results.csv
```

### 3. PSLQ Verification

```python
from s42 import verify_pslq_identity

residual, coeffs = verify_pslq_identity(
    x=0.5,
    precision=200,
    verbose=True
)
```

### 4. Adding New Identity

1. Discover via PSLQ:
   ```python
   from s42.pslq import find_pslq_relation
   from s42.basis import compute_omega2_basis
   from s42.series import S42_series
   
   mp.dps = 200
   target = S42_series(x=1/3, max_terms=600000)
   basis = compute_omega2_basis(precision=200)
   coeffs = find_pslq_relation(target, basis)
   ```

2. Add to `coefficients.py`

3. Create JSON file in `data/coefficients/`

4. Add tests

5. Submit pull request

## Performance Considerations

### Basis Computation
- **One-time cost**: O(p²) where p is precision
- **Typical times**: 50 dps → ~50ms, 120 dps → ~200ms, 200 dps → ~1s
- **Recommendation**: Precompute once, reuse for multiple evaluations

### Series Evaluation
- **Cost**: O(n) where n is number of terms needed
- **Terms needed**: ~p (precision-dependent)
- **Typical times**: 120 dps → ~3ms

### Closed Form
- **Per-evaluation cost**: O(1) (21 multiply-adds)
- **Typical times**: 120 dps → ~150μs
- **Crossover**: Beneficial after ~20-30 evaluations

### GPU Acceleration
- **Batch sizes**: 1K-100K elements
- **Speedup**: 39×-241× for large batches
- **Precision**: Limited to float32 on Apple MPS

## File Formats

### Coefficients JSON
```json
{
  "x_value": "1/2",
  "description": "S₄,₂(1/2) identity",
  "coefficients": [
    {"numerator": 15683, "denominator": 14280, "basis": "ζ(6)"},
    ...
  ],
  "metadata": {
    "pslq_residual": "2.7e-98",
    "precision": 200,
    "date_discovered": "2026-01-11"
  }
}
```

### Benchmark Results CSV
```csv
x,precision,series_time_ms,closed_time_us,speedup,abs_error
0.5,120,3.356,155.553,21.6,2.7e-98
```

## Dependencies

### Core
- mpmath: Arbitrary precision arithmetic
- numpy: Array operations
- scipy: Scientific computing

### Visualization
- matplotlib: Plotting
- seaborn: Statistical visualization

### Optional
- torch: GPU acceleration
- sympy: Symbolic mathematics

### Development
- pytest: Testing
- black, isort, flake8: Code quality
- mypy: Type checking

## Documentation

- **README.md**: Quick start and overview
- **CONTRIBUTING.md**: Contribution guidelines
- **API.md**: Detailed API documentation
- **MATHEMATICAL_DETAILS.md**: Mathematical background
- **COMPUTATIONAL_NOTES.md**: Implementation notes

## Getting Help

- Documentation: `docs/`
- Examples: `notebooks/`
- Scripts: `scripts/quick_start.py`
- Tests: `tests/` (show usage patterns)
- Issues: GitHub issue tracker
- Discussions: GitHub discussions

## Version History

See CHANGELOG.md for detailed version history.

## License

MIT License - see LICENSE file
