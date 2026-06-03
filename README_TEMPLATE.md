# S42 Corrected Reproducibility README Template

This template reflects the corrected revision of the S_{4,2}(x) work.

## Corrected claims

- `x = 1/2`: corrected exact closed form in a 13-element dyadic weight-6 basis.
- `x = 1/4`: certified exact relation in a depth-2 multiple-polylogarithm basis; this is not a reduction to independently known constants.
- `x = -1/2`: open; no certified closed form is implemented.

## Deprecated claims that must not be reintroduced

- exact closed forms at all three dyadic arguments;
- the withdrawn 21-element Omega2 basis;
- Clausen constants at pi/3 as dyadic reduction constants;
- single-precision/single-residual exactness certification.

## Reproducibility standard

A relation is accepted only when the residual tracks increasing working precision and coefficients remain stable across precision levels.
