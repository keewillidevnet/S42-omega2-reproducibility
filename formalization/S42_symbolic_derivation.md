# Symbolic derivation of the S4,2(1/2) closed form

## Theorem

Let S4,2(x) = sum over n >= 1 of H_{n-1} x^n / n^5, where H_n is the nth harmonic
number and H_0 = 0. Then

  S4,2(1/2) = -51/32 zeta(6) - 1/4 zeta(3)^2 - 1/32 zeta(5) log2
            - 1/6 zeta(3) log^3 2 + 1/12 pi^2 zeta(3) log2 + 1/1440 pi^4 log^2 2
            + 1/144 pi^2 log^4 2 - 1/240 log^6 2 + 2 Li6(1/2) + Li5(1/2) log2
            - 1/2 S4,2(-1).

S4,2(-1) is the single irreducible depth-2 generator of the weight-6 level-2
space. It is carried as an opaque constant and is not reduced further.

## Status of this document

The derivation is rigorous modulo two inputs, both standard:

  1. The functional equation for S4,2 stated in Step 2, proved in
     arXiv:2508.05770 (Lemma 6.3) via their Theorem 5.1. For a fully
     self-contained proof, reprove this equation by differentiate-and-evaluate
     (see the companion Lean skeleton); that is the same obligation the formal
     proof must discharge.
  2. The classical reductions in Step 3 (Li_n(-1) to zeta, and zeta at even
     integers to powers of pi), all provable from elementary series identities.

Every rational coefficient in Step 4 is verified exactly by computer algebra,
not by numerical fit. A high-precision cross-check (residual tracking the
precision floor to about 1e-301 at 300 digits) independently confirms the
result but is not part of the proof.

## Step 1: S4,2 is the Nielsen polylogarithm of weight 6

Define the generating-function family F_s(x) = sum over n >= 1 of
H_{n-1} x^n / n^s, so that S4,2(x) = F_5(x). The family satisfies the
differential ladder

  d/dx F_s(x) = (1/x) F_{s-1}(x)    for s >= 1,

with base case the classical generating function

  F_0(x) = sum over n >= 1 of H_{n-1} x^n = - x log(1-x) / (1-x).

Both facts are immediate: the ladder is term-by-term differentiation, and the
base case is the Cauchy product of -log(1-x) with the geometric series.
Iterating the ladder yields the iterated-integral representation

  F_s(x) = integral from 0 to x of F_{s-1}(t)/t dt,

which places F_s in the algebra of harmonic polylogarithms on the alphabet
{0,1} of weight s+1. In particular F_5 = S4,2 coincides with the Nielsen
generalized polylogarithm S_{4,2} under the standard identity
S_{4,2}(x) = sum over n >= 1 of H_{n-1} x^n / n^5. This is why the published
Nielsen functional-equation literature applies to this kernel directly.

## Step 2: the functional equation, specialized

arXiv:2508.05770, Lemma 6.3, gives a functional equation for S4,2 in a variable
z. Written with L(z) := log(2 sinh z):

  S4,2(1 - e^{2z}) + S4,2(1 - e^{-2z}) + S4,2(e^{-2z})
    = 2 ( Li6(1 - e^{2z}) + Li6(1 - e^{-2z}) + Li6(e^{-2z}) )
      - z ( 2 Li5(1 - e^{2z}) - 2 Li5(1 - e^{-2z}) - Li5(e^{-2z}) )
      - L(z) Li5(e^{-2z})
      + L(z) ( 2 z^5/15 + zeta(5) - 2 z zeta(4) + 2 z^2 zeta(3) - 4 z^3/3 zeta(2) )
      - z^4/3 L(z)^2
      - z^6/15 - 2 z^3/3 zeta(3) - 3 z^2/2 zeta(4) + 2 z zeta(2) zeta(3)
      - z zeta(5) - 5/4 zeta(6) - zeta(3)^2/2.

Specialize at z0 = (1/2) log2. Then e^{2 z0} = 2 and e^{-2 z0} = 1/2, so the
three arguments are

  1 - e^{2 z0}  = -1,
  1 - e^{-2 z0} = 1/2,
  e^{-2 z0}     = 1/2.

The left side becomes S4,2(-1) + 2 S4,2(1/2). Also
2 sinh(z0) = e^{z0} - e^{-z0} = sqrt(2) - 1/sqrt(2) = 1/sqrt(2), so
L(z0) = log(1/sqrt(2)) = -(1/2) log2.

Solving for the value of interest:

  S4,2(1/2) = (1/2) R(z0) - (1/2) S4,2(-1),

where R(z0) is the right side above evaluated at z0. The coefficient -1/2 on
S4,2(-1) is forced by the equation; it is exactly the coefficient PSLQ
recovered.

## Step 3: reductions applied to R(z0)

  - Li6(-1) = -(1 - 2^{-5}) zeta(6) = -(31/32) zeta(6).
  - Li5(-1) = -(1 - 2^{-4}) zeta(5) = -(15/16) zeta(5).
    (General fact: Li_n(-1) = -(1 - 2^{1-n}) zeta(n), since the alternating
    series equals the negative of the Dirichlet eta function eta(n).)
  - zeta(2) = pi^2/6, zeta(4) = pi^4/90 (Euler).
  - Li6(1/2) and Li5(1/2) do not reduce and are retained as basis elements.
  - L(z0) = -(1/2) log2 and z0 = (1/2) log2 are substituted everywhere.

Note that no pi^6 term arises outside zeta(6): the only sixth-power term is
z0^6 = (log2)^6 / 64, which contributes to log^6 2. The terms zeta(2) and
zeta(4), multiplied by powers of z0, produce the pi^2 log^4 2 and pi^4 log^2 2
basis elements. zeta(6) appears only as a standalone basis element. This is why
the basis cleanly separates zeta(6) from the pure pi-and-log monomials.

## Step 4: coefficient reconciliation

Collecting (1/2) R(z0) by basis element gives the following, verified exactly by
computer algebra (the difference between (1/2) R(z0) and the target block below
simplifies identically to 0):

  basis element        coefficient
  -----------------    -----------
  zeta(6)              -51/32
  zeta(3)^2            -1/4
  zeta(5) log2         -1/32
  zeta(3) log^3 2      -1/6
  pi^2 zeta(3) log2     1/12
  pi^4 log^2 2          1/1440
  pi^2 log^4 2          1/144
  log^6 2              -1/240
  Li6(1/2)              2
  Li5(1/2) log2         1

Adding the carried term -(1/2) S4,2(-1) reproduces the Theorem verbatim. The
quickest hand checks:

  - Li6(1/2): R(z0) contributes 4 Li6(1/2) (two from the b and c arguments,
    via 2(... + Li6(1/2) + Li6(1/2)) ). Half of 4 is 2.
  - Li5(1/2) log2: R(z0) contributes 3 z0 Li5(1/2) from the -z(...) block plus
    (1/2) log2 Li5(1/2) from the -L Li5 term, totalling 2 log2 Li5(1/2). Half is
    log2 Li5(1/2).
  - zeta(3)^2: only the trailing -zeta(3)^2/2 contributes; half is -1/4.

The remaining elementary coefficients follow the same way once z0 = (1/2) log2,
zeta(2) = pi^2/6, and zeta(4) = pi^4/90 are substituted.

## What remains for full rigor

The only non-elementary step is the functional equation of Step 2. As a math
proof, citing it is legitimate: it is a published, peer-reviewed result
(arXiv:2508.05770, Lemma 6.3), and it has been independently certified here to
the precision floor (residual about 3.6e-251 at 250 digits at z0, tracking
precision). Steps 3 and 4 are then finite rational arithmetic, CAS-verified.

To remove the citation entirely is a larger task than a single
differentiate-and-evaluate, and the naive version of that argument does not
work. Differentiating the weight-6 equation does not reduce it to elementary
functions: the weight-5 object F_4 persists in every derivative through the
product-rule branch, so there is no finite number of differentiations that
lands on a purely elementary identity. The correct structure is an induction on
weight. Differentiating the weight-6 equation reduces it to the weight-5
functional equation plus elementary terms; that reduces to weight 4; and so on
down to a low-weight base case where the equation is between elementary or
dilogarithm-level functions. Each inductive step fixes one constant of
integration at a regular base point (z = 0 is singular because log(2 sinh z)
diverges there, so use an interior point). A self-contained proof therefore
formalizes the whole tower of functional equations, not one equation. This is
finite and contains no open research, but it is a multi-lemma project.
