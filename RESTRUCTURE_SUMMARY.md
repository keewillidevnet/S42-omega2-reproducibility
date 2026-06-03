# Corrected Revision Restructure Summary

This repo has been updated from the withdrawn v1 narrative to the corrected revision.

## Removed / deprecated

- v1 21-element Ω₂ basis
- level-6 Clausen constants at `π/3`
- exact closed-form claims for `x=1/4` and `x=-1/2`
- coefficient vectors that plateau near `1e-98`

## Added / corrected

- 13-element weight-6 level-2 dyadic basis for `S_{4,2}(1/2)`
- corrected exact coefficient vector for `S_{4,2}(1/2)`
- certified depth-2 MPL relation for `S_{4,2}(1/4)`
- explicit open status for `S_{4,2}(-1/2)`
- tests verifying the corrected implementation against direct series evaluation

## Important terminology

Use **closed form** only for `x=1/2`.
Use **certified exact relation** for `x=1/4`.
Use **open** for `x=-1/2`.
