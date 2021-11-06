#!/usr/bin/env python3

# We add an error band to the x-has-errors lsqfit example,
#     https://lsqfit.readthedocs.io/en/latest/overview.html#x-has-errors

####
####    As in the lsqfit docs:
####


import gvar as gv
import lsqfit

def make_data():
    x = gv.gvar([
        '0.73(50)',   '2.25(50)',  '3.07(50)',  '3.62(50)',  '4.86(50)',
        '6.41(50)',   '6.39(50)',  '7.89(50)',  '9.32(50)',  '9.78(50)',
        '10.83(50)', '11.98(50)', '13.37(50)', '13.84(50)', '14.89(50)'
        ])
    y = gv.gvar([
         '3.85(70)',  '5.5(1.7)',  '14.0(2.6)',   '21.8(3.4)',   '47.0(5.2)',
        '79.8(4.6)', '84.9(4.6)',  '95.2(2.2)',   '97.65(79)',   '98.78(55)',
        '99.41(25)', '99.80(12)', '100.127(77)', '100.202(73)', '100.203(71)'
        ])
    return x,y

def make_prior(x):
    prior = gv.BufferDict()
    prior['b'] = gv.gvar(['200(500)', '0(5)', '0(5)', '0(5)'])
                        #  ^ central value is a change from lsqfit docs.
                        #    If I picked 0(500) I got a TERRIBLE fit.
    prior['x'] = x
    return prior

def fcn(p):
    b0, b1, b2, b3 = p['b']
    x = p['x']
    return b0 / ((1. + gv.exp(b1 - b2 * x)) ** (1. / b3))


x, y = make_data()
prior = make_prior(x)
fit = lsqfit.nonlinear_fit(prior=prior, data=y, fcn=fcn)
print(fit)

####
####    Begin plotting.
####

import numpy as np
import matplotlib.pyplot as plt
import gvarplot

# Plot the evidence
fix, ax = plt.subplots(1,1, squeeze=True)
gvarplot.errorbar(ax, x, y, linestyle='None')

# To overlay the best-fit result
result = {'b': fit.p['b']}      # we take the fit parameters
X = np.linspace(0,15,1000)      # and scan on x.
best_fit = fcn({**result, 'x': X})

gvarplot.errorbar(ax, X, best_fit, sigma=[1,2,3], marker=',', color='red', alpha=1.0/16, zorder=-1)

ax.set_xlabel('x')
ax.set_ylabel('y')

gvarplot.uncertainty_matrix(result['b'], labels='b')

plt.show()
