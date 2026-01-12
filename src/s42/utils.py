"""
Utility Functions
=================

Helper functions for S₄,₂(x) computation.
"""

from mpmath import mp, mpf, fabs
from typing import List, Tuple


def harmonic(n: int, precision: int = None) -> mpf:
    """
    Compute the nth harmonic number H_n = 1 + 1/2 + ... + 1/n.
    
    Args:
        n: Index
        precision: Decimal precision (default: current mp.dps)
    
    Returns:
        H_n as mpf
    
    Example:
        >>> from mpmath import mp
        >>> mp.dps = 50
        >>> H_10 = harmonic(10)
        >>> print(H_10)  # ≈ 2.928968...
    """
    if precision is not None:
        old_dps = mp.dps
        mp.dps = precision
    
    try:
        result = mpf(0)
        for k in range(1, n + 1):
            result += mpf(1) / mpf(k)
        return result
    finally:
        if precision is not None:
            mp.dps = old_dps


def harmonic_vectorized(n_max: int, precision: int = None) -> List[mpf]:
    """
    Compute H_1, H_2, ..., H_n_max efficiently.
    
    Uses accumulation: H_n = H_{n-1} + 1/n
    
    Args:
        n_max: Maximum index
        precision: Decimal precision
    
    Returns:
        List [H_1, H_2, ..., H_n_max]
    """
    if precision is not None:
        old_dps = mp.dps
        mp.dps = precision
    
    try:
        harmonics = []
        H = mpf(0)
        
        for n in range(1, n_max + 1):
            H += mpf(1) / mpf(n)
            harmonics.append(H)
        
        return harmonics
    finally:
        if precision is not None:
            mp.dps = old_dps


def convergence_check(
    terms: List[mpf],
    threshold: float = None,
    window: int = 35
) -> Tuple[bool, int]:
    """
    Check if a sequence has converged.
    
    Returns True if the last `window` terms are all below threshold.
    
    Args:
        terms: List of term magnitudes
        threshold: Convergence threshold (default: 10^(-dps-10))
        window: Number of consecutive small terms required
    
    Returns:
        Tuple of (converged, index_of_convergence)
    """
    if threshold is None:
        threshold = mpf(10) ** (-(mp.dps + 10))
    
    if len(terms) < window:
        return False, -1
    
    # Check last `window` terms
    for i in range(len(terms) - window, len(terms)):
        if fabs(terms[i]) >= threshold:
            return False, -1
    
    return True, len(terms) - window


def format_mpf(value: mpf, decimal_places: int = None, scientific: bool = False) -> str:
    """
    Format an mpf value for display.
    
    Args:
        value: The mpf value
        decimal_places: Number of decimal places (default: mp.dps)
        scientific: Use scientific notation
    
    Returns:
        Formatted string
    """
    if decimal_places is None:
        decimal_places = mp.dps
    
    if scientific:
        return mp.nstr(value, decimal_places, strip_zeros=False)
    else:
        return str(value)[:decimal_places + 10]  # Extra for sign, decimal point


def relative_error(computed: mpf, reference: mpf) -> mpf:
    """
    Compute relative error.
    
    Args:
        computed: Computed value
        reference: Reference value
    
    Returns:
        |computed - reference| / |reference|
    """
    if reference == 0:
        return mpf('inf') if computed != 0 else mpf(0)
    
    return fabs(computed - reference) / fabs(reference)


def estimate_precision_needed(target_accuracy: float) -> int:
    """
    Estimate decimal precision needed to achieve target accuracy.
    
    Args:
        target_accuracy: Target absolute accuracy (e.g., 1e-100)
    
    Returns:
        Recommended decimal precision
    """
    from math import log10, ceil
    
    # Need extra precision for intermediate calculations
    safety_margin = 20
    
    # Convert accuracy to decimal places
    if target_accuracy > 0:
        decimal_places = -log10(target_accuracy)
    else:
        decimal_places = 100  # Default
    
    return ceil(decimal_places) + safety_margin


def timer(func):
    """
    Decorator to time function execution.
    
    Example:
        @timer
        def slow_function():
            # ...
    """
    import time
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        print(f"{func.__name__} took {elapsed*1000:.3f} ms")
        return result
    
    return wrapper


def progress_bar(iterable, desc: str = "", total: int = None):
    """
    Simple progress bar for loops.
    
    Uses tqdm if available, otherwise plain iteration.
    
    Args:
        iterable: The iterable to wrap
        desc: Description text
        total: Total iterations (if not inferrable)
    """
    try:
        from tqdm import tqdm
        return tqdm(iterable, desc=desc, total=total)
    except ImportError:
        return iterable


def save_to_json(data: dict, filename: str) -> None:
    """
    Save data to JSON file with mpf handling.
    
    Args:
        data: Dictionary to save
        filename: Output filename
    """
    import json
    
    # Convert mpf to string
    def convert_mpf(obj):
        if isinstance(obj, mpf):
            return str(obj)
        elif isinstance(obj, dict):
            return {k: convert_mpf(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_mpf(item) for item in obj]
        else:
            return obj
    
    data_converted = convert_mpf(data)
    
    with open(filename, 'w') as f:
        json.dump(data_converted, f, indent=2)


def load_from_json(filename: str, convert_to_mpf: bool = True) -> dict:
    """
    Load data from JSON file with optional mpf conversion.
    
    Args:
        filename: Input filename
        convert_to_mpf: Convert numeric strings back to mpf
    
    Returns:
        Loaded data dictionary
    """
    import json
    
    with open(filename, 'r') as f:
        data = json.load(f)
    
    if convert_to_mpf:
        def try_convert(obj):
            if isinstance(obj, str):
                try:
                    return mpf(obj)
                except:
                    return obj
            elif isinstance(obj, dict):
                return {k: try_convert(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [try_convert(item) for item in obj]
            else:
                return obj
        
        data = try_convert(data)
    
    return data


def benchmark_function(func, *args, num_trials: int = 10, **kwargs) -> dict:
    """
    Benchmark a function with multiple trials.
    
    Args:
        func: Function to benchmark
        *args: Positional arguments for func
        num_trials: Number of trials
        **kwargs: Keyword arguments for func
    
    Returns:
        Dictionary with timing statistics
    """
    import time
    import numpy as np
    
    times = []
    
    for _ in range(num_trials):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        times.append(elapsed)
    
    times = np.array(times)
    
    return {
        "mean": np.mean(times),
        "std": np.std(times),
        "min": np.min(times),
        "max": np.max(times),
        "median": np.median(times),
        "num_trials": num_trials,
        "result": result,
    }


if __name__ == "__main__":
    # Demonstration
    print("Utility Functions Demo")
    print("=" * 70)
    
    # Harmonic numbers
    print("\nHarmonic numbers:")
    mp.dps = 50
    for n in [1, 5, 10, 50, 100]:
        H_n = harmonic(n)
        print(f"  H_{n:3d} = {H_n}")
    
    # Convergence check
    print("\nConvergence check:")
    terms = [mpf(10) ** (-i) for i in range(100)]
    converged, idx = convergence_check(terms, threshold=mpf(1e-50), window=35)
    print(f"  Converged: {converged}, at index: {idx}")
    
    # Precision estimation
    print("\nPrecision estimation:")
    for accuracy in [1e-50, 1e-100, 1e-200]:
        prec = estimate_precision_needed(accuracy)
        print(f"  For accuracy {accuracy:.0e}: need {prec} decimal places")
