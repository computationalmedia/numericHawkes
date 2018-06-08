from tick.hawkes import SimuInhomogeneousPoisson # SimuHawkes,HawkesKernelTimeFunc
import numpy as np
import scipy.integrate as integrate

class Hawkes:
    def __init__(self,baseline,kernel):
        self.kernel = kernel
        self.baseline = baseline
        
    def intensity(self,history,t):
        """ History: [ [x1,x2,...], [mark11,mark12,...], [mark21,mark22,...] ]
        """
        t_diff = t - history[0]
        t_diff = t_diff[t_diff>0]
        y = self.baseline+sum([self.kernel(td) for td in t_diff])
        return y

    def log_likelihood(self,history):
        integral = integrate.quad(lambda x: self.intensity(history,x),0,events[-1])[0]
        log = sum([np.log(self.intensity(events,e)) for e in events])
        ll = log-integral
        return ll
    
    def simulation(self,run_time,seed=None):
        """
            hawkes = SimuHawkes(baseline=self.baseline, end_time=run_time, verbose=False, seed=seed)
            kernel = HawkesKernelTimeFunc(self.kernel)
            hawkes.set_kernel(0,0,kernel) # only support one-dimensional Hawkes
            hawkes.simulate()
            return hawkes.timestamps[0]
        """
        n = 0
        D = []
        def _s(i, x0):
            f = self.baseline if i == 0 else self.kernel
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
        
        t = sorted([e[1] for e in D]) # time
        D = [(t.index(D[e[0]-1][1])+1 if e[0]>0 else 0, e[1]) for e in D]
        p = {}
        # parent relations
        for i in range(n):
            if D[i][0] in p: 
                p[D[i][0]].append(i+1)
            else:
                p[D[i][0]] = [i+1]
        
        # xs = []
        # for i in xs_dict:
        #     xs.append(sorted(xs_dict[i]))
        
        return t,p
    
    def branching_factor(self, upper=None):
        return integrate.quad(lambda x: self.kernel.value(x),0,upper)[0]
    
    
