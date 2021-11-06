#!/usr/bin/env python3

# Add plotting to the lsqfit introductory fit.
#     https://lsqfit.readthedocs.io/en/latest/overview.html#introduction

####
####    As in the lsqfit docs:
####

import numpy as np
import gvar as gv
import lsqfit

y = {                                 # data for the dependent variable
   'data1' : gv.gvar([1.376, 2.010], [[ 0.0047, 0.01], [ 0.01, 0.056]]),
   'data2' : gv.gvar([1.329, 1.582], [[ 0.0047, 0.0067], [0.0067, 0.0136]]),
   'b/a'   : gv.gvar(2.0, 0.5)
   }
x = {                                 # independent variable
   'data1' : np.array([0.1, 1.0]),
   'data2' : np.array([0.1, 0.5])
   }
prior = {}
prior['a'] = gv.gvar(0.5, 0.5)
prior['b'] = gv.gvar(0.5, 0.5)

def fcn(x, p):                        # fit function of x and parameters p
  ans = {}
  for k in ['data1', 'data2']:
     ans[k] = gv.exp(p['a'] + x[k] * p['b'])
  ans['b/a'] = p['b'] / p['a']
  return ans

# do the fit
fit = lsqfit.nonlinear_fit(data=(x, y), prior=prior, fcn=fcn, debug=True)
print(fit.format(maxline=True))       # print standard summary of fit

p = fit.p                             # best-fit values for parameters
outputs = dict(a=p['a'], b=p['b'])
outputs['b/a'] = p['b']/p['a']
inputs = dict(y=y, prior=prior)
print(gv.fmt_values(outputs))              # tabulate outputs
print(gv.fmt_errorbudget(outputs, inputs)) # print error budget for outputs


####
####    Plot with gvarplot
####

import matplotlib.pyplot as plt
import gvarplot

fig, ax = plt.subplots(1,1,squeeze=True)
gvarplot.errorbar(ax, x['data1'], y['data1'])
gvarplot.errorbar(ax, x['data2'], y['data2'])

X = {
        'data1': np.linspace(0,1,1000),
        'data2': np.linspace(0,1,1000),
        }
Y = fcn(X, outputs)

gvarplot.errorbar(ax, X['data1'], Y['data1'], color='gray', alpha=0.1, zorder=-1)

params = ['a', 'b', 'b/a']
gvarplot.uncertainty_matrix([outputs[o] for o in params], labels=params)

plt.show()
