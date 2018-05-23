from tick.hawkes import SimuInhomogeneousPoisson

def simulation(phi, mu, run_time):
    n = 0
    D = []
    def _s(i, x0):
        f = mu if i == 0 else phi
        poisson = SimuInhomogeneousPoisson([f], end_time=run_time-x0, verbose=False)
        poisson.simulate()
        X = poisson.timestamps[0]
        n = i
        for x in X:
            n = n + 1
            D.append((i, x0 + x))
            n = _s(n, x0 + x)
        return n

    n = _s(0, 0)
    return D