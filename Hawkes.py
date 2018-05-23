from tick.hawkes import (SimuHawkes,HawkesKernelTimeFunc)
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
        hawkes = SimuHawkes(baseline=self.baseline, end_time=run_time, verbose=False, seed=seed)
        kernel = HawkesKernelTimeFunc(self.kernel)
        hawkes.set_kernel(0,0,kernel) # only support one-dimensional Hawkes
        hawkes.simulate()
        return hawkes.timestamps[0]
    
    def branching_factor(self, upper=None):
        return integrate.quad(lambda x: self.kernel.value(x),0,upper)[0]
    
    
