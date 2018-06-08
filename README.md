# numericalHawkes

This repository contains:

- A discrete implementation of the Hawkes process.
- A simulation for the Hawkes process which returns the branching structure.
- A demo showing how to use this code.

# Usage:

## Required packages:

  - python3
  - numpy
  - scipy
  - [tick](https://github.com/X-DataInitiative/tick)

## Tutorial:

### Preliminary
Load tick.base.TimeFunction, Hawkes and numpy.

```python
from tick.base import TimeFunction
from Hawkes import Hawkes
import numpy as np
```

### Define a Hawkes process
The baseline and triggering kernel are defined by tick.base.TimeFunction. Both functions are defined piecewise (discrete). 

For example, a power function on ![](https://latex.codecogs.com/gif.latex?%5Cinline%20%5Cdpi%7B100%7D%20%5Cfn_cm%20%5B0%2C%5Cpi%5D) can be realized as

![](https://latex.codecogs.com/gif.latex?%5Cfn_cm%20%5Csmall%20f%28x%29%20%3D%20%5Cdfrac%7B0.21%7D%7B%28x&plus;0.05%29%5E%7B1.1%7D%7D)

```python
ts = np.append([0],np.logspace(-5,np.log10(np.pi),256))
ys = 0.21/(ts+0.05)**1.1
phi = TimeFunction([ts, ys], inter_mode=TimeFunction.InterConstRight, dt=1e-6)
mu = TimeFunction([ts, 5*np.ones(len(ts))], inter_mode=TimeFunction.InterConstRight, dt=1e-6)
hawkes = Hawkes(mu,phi)
```
### Simulation
The simulation returns a time sequence and the corresponding triggering relations.

```python
t,p = hawkes.simulation(np.pi)
```

# Todo
- Test
