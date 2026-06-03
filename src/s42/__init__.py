"""S_{4,2} corrected reproducibility package."""

__version__ = "1.1.0"
__author__ = "Keenan Williams"

from .series import evaluate_series, S42_series
from .closed_form import evaluate_relation, evaluate_closed_form, S42_closed_form
from .basis import (
    compute_dyadic_w6_basis,
    compute_quarter_relation_basis,
    compute_basis_for_x,
    DYADIC_W6_BASIS_NAMES,
    QUARTER_RELATION_BASIS_NAMES,
    compute_omega2_basis,
    OMEGA2_BASIS_NAMES,
)
from .coefficients import get_coefficients, get_relation_status, AVAILABLE_X_VALUES, OPEN_X_VALUES

__all__ = [
    "evaluate_series", "S42_series", "evaluate_relation", "evaluate_closed_form", "S42_closed_form",
    "compute_dyadic_w6_basis", "compute_quarter_relation_basis", "compute_basis_for_x",
    "DYADIC_W6_BASIS_NAMES", "QUARTER_RELATION_BASIS_NAMES", "compute_omega2_basis",
    "OMEGA2_BASIS_NAMES", "get_coefficients", "get_relation_status", "AVAILABLE_X_VALUES", "OPEN_X_VALUES",
]
