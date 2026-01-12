"""
S₄,₂(x) Euler Sum Package
=========================

Exact closed-form identities for the weight-6 Euler sum S₄,₂(x) at rational points.

Main functions:
- evaluate_series: Compute S₄,₂(x) via direct series summation
- evaluate_closed_form: Compute S₄,₂(x) via exact Ω₂ identity
- compute_omega2_basis: Compute the 21-element weight-6 constant basis
- verify_pslq_identity: Verify PSLQ-discovered coefficients

Example usage:
    >>> from s42 import evaluate_series, evaluate_closed_form
    >>> from mpmath import mp
    >>> mp.dps = 120
    >>> value = evaluate_closed_form(x=0.5)
    >>> print(value)
"""

__version__ = "1.0.0"
__author__ = "Keenan Williams"
__email__ = "your-email@example.com"

from .series import evaluate_series, S42_series
from .closed_form import evaluate_closed_form, S42_closed_form
from .basis import compute_omega2_basis, OMEGA2_BASIS_NAMES
from .coefficients import get_coefficients, AVAILABLE_X_VALUES
from .pslq import verify_pslq_identity, find_pslq_relation
from .utils import harmonic, convergence_check

__all__ = [
    # Core evaluation functions
    "evaluate_series",
    "evaluate_closed_form",
    "S42_series",
    "S42_closed_form",
    
    # Basis computation
    "compute_omega2_basis",
    "OMEGA2_BASIS_NAMES",
    
    # Coefficients
    "get_coefficients",
    "AVAILABLE_X_VALUES",
    
    # PSLQ verification
    "verify_pslq_identity",
    "find_pslq_relation",
    
    # Utilities
    "harmonic",
    "convergence_check",
]
