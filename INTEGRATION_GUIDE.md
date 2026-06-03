# Integration Guide — Corrected Revision

## Evaluate the corrected `x=1/2` closed form

```python
from mpmath import mp
from s42 import evaluate_relation

mp.dps = 100
value = evaluate_relation(0.5)
```

## Evaluate the certified `x=1/4` depth-2 relation

```python
from mpmath import mp
from s42 import evaluate_relation, get_relation_status

mp.dps = 100
print(get_relation_status(0.25))
value = evaluate_relation(0.25)
```

This is not a reduction to independently known constants. The basis contains unreduced depth-2 MPLs, including `Li_{5,1}(-1/2)`.

## Open case

```python
from s42 import evaluate_relation

evaluate_relation(-0.5)  # raises ValueError
```

`S_{4,2}(-1/2)` remains open in the corrected revision.
