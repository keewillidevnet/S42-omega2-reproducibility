# Contributing to S₄,₂ Euler Sum Project

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/S42-omega2-reproducibility.git
   cd S42-omega2-reproducibility
   ```
3. **Set up the development environment**:
   ```bash
   python -m venv s42env
   source s42env/bin/activate  # On Windows: s42env\Scripts\activate
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   ```

## Types of Contributions

### 1. New Euler Sum Identities

We welcome contributions of new exact identities for:
- S₄,₂(x) at additional x values (e.g., x = 1/3, 1/8)
- Other weight-6 Euler sums (e.g., S₃,₃, S₅,₁)
- Higher-weight sums

**Requirements:**
- PSLQ residual < 10⁻⁹⁶
- Working precision ≥ 200 decimal places
- Exact rational coefficients
- Independent verification

**Submission format:**
```python
# data/coefficients/s42_third.json
{
  "x_value": "1/3",
  "coefficients": [
    {"numerator": 123, "denominator": 456},
    ...
  ],
  "pslq_residual": "1.23e-98",
  "verification_precision": 200
}
```

### 2. Performance Improvements

- Faster series evaluation algorithms
- Optimized basis computation
- GPU/TPU kernels for batch evaluation
- Better convergence acceleration

**Please include:**
- Benchmark results comparing old vs new
- Tests verifying numerical correctness
- Documentation of algorithm changes

### 3. Bug Fixes

Found a bug? Please:
1. Check if it's already reported in [Issues](https://github.com/keewillidevnet/S42-omega2-reproducibility/issues)
2. Create a new issue if not, with:
   - Minimal reproducible example
   - Expected vs actual behavior
   - System information (OS, Python version)
3. Submit a pull request with:
   - Fix for the bug
   - Test case that would have caught it
   - Update to documentation if needed

### 4. Documentation

Improvements to:
- README clarity
- API documentation
- Jupyter notebooks
- Mathematical explanations

### 5. Tests

We aim for high test coverage. Contributions of tests are always welcome, especially:
- Edge cases
- Numerical stability tests
- Cross-validation with other systems (Mathematica, Maple)

## Development Workflow

### Code Style

We use:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Before committing:
```bash
black src/ scripts/ tests/
isort src/ scripts/ tests/
flake8 src/ scripts/ tests/
mypy src/
```

Or use pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

### Testing

Run tests before submitting:
```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src/s42 --cov-report=html

# Specific test
pytest tests/test_basis.py::test_omega2_basis -v
```

### Branch Strategy

- `main`: Stable, released code
- `develop`: Integration branch for new features
- `feature/*`: Individual feature branches
- `fix/*`: Bug fix branches

### Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/new-identity-x-third
   ```

2. **Make your changes**:
   - Write code
   - Add tests
   - Update documentation
   - Run tests locally

3. **Commit with clear messages**:
   ```bash
   git commit -m "Add S₄,₂(1/3) identity with PSLQ verification"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/new-identity-x-third
   ```

5. **Create Pull Request**:
   - Go to the GitHub repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the template

### Pull Request Checklist

- [ ] Code follows project style (black, isort, flake8)
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or clearly documented if necessary)

## Mathematical Contributions

### PSLQ Discovery Process

When discovering new identities:

1. **Compute target value** at high precision (200+ digits):
   ```python
   mp.dps = 200
   target = S42_series(x, max_terms=600000)
   ```

2. **Compute basis** at same precision:
   ```python
   basis = compute_omega2_basis(precision=200)
   ```

3. **Run PSLQ**:
   ```python
   relation = mp.pslq([target] + basis, maxcoeff=100000)
   ```

4. **Verify residual** < 10⁻⁹⁶

5. **Extract rational coefficients** and verify they're exact

6. **Cross-verify** at different precisions (250, 300 digits)

### Symbolic Verification

If possible, verify identities symbolically using:
- Mathematica
- Maple
- SymPy

Include verification scripts in `tests/symbolic/`.

## Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:
- Be respectful and constructive
- Welcome newcomers
- Focus on what's best for the community
- Show empathy towards other community members

### Getting Help

- **Questions**: Open a [Discussion](https://github.com/keewillidevnet/S42-omega2-reproducibility/discussions)
- **Bugs**: Open an [Issue](https://github.com/keewillidevnet/S42-omega2-reproducibility/issues)
- **Security**: Email maintainer directly (see README)

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Acknowledged in paper updates
- Credited in release notes

Significant contributions (new identities, major features) will be discussed for co-authorship on future publications.

## License

By contributing, you agree that your contributions will be licensed under the same MIT License as the project.

## Questions?

Feel free to reach out:
- Open a Discussion on GitHub
- Email: [your-email]
- Twitter: [@your-handle]

Thank you for contributing to advancing computational mathematics! 🎓
