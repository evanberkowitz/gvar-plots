#!/usr/bin/env python3

import gvar as gv
import lsqfit as lsf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch

import gvarplot

# Suppose we are an astronomer and have observed the orbit of some planet
# at various points along its orbit.  We want to extract orbital parameters
# so that we know where to point our telescopes for future observations.

# (Classical) Orbits are ellipses to very good approximation.

# An ellipse is a conic section that satisfies
#
#   ( (x-x0)/a )^2 + ( (y-y0)/b )^2 = 1
#
# It is has a center at (x0, y0)
# and maximal distances a and b.
# Finally, we can rotate the figure set by a, b, x0, and y0 by any phi.
def ellipse(a, b, phi=0, x0=0, y0=0, **kwargs):
    # When we specify the parameters, we are left with a function of an angle
    # theta = (-pi, +pi]
    def curried(theta):
        return np.array([
                x0 + a*np.cos(theta)*np.cos(phi) - b*np.sin(theta)*np.sin(phi),
                y0 + b*np.sin(theta)*np.cos(phi) + a*np.cos(theta)*np.sin(phi)
               ])
    return curried

theta = np.arange(-np.pi, +np.pi, 0.005)


# We need to make up some data that comes from an ellipse 
# with errors + uncertainties.
# Our data will be made up with the underlying data.
underlying = {
    # These are the 'true' parameters of the orbit.
    # But, once we generate the some synthetic observational data,
    # We can never check these parameters again.
    'a':3,
    'b':1,
    'phi':0.2,
    'x0':10,
    'y0':12,
}

e = ellipse(**underlying) # the function we hope to recover.
exact = e(theta)          # numerical values with the exact underlying parameters
# Now that we have some definitive orbit, we need to 'observe' it by 
# making up some synthetic data.
# Now we need some random thetas at which to place made-up data.
SEED=42             # Change for different universes.
OBSERVATIONS=20     # Adjust to add or subtract observations
rng = np.random.default_rng(seed=SEED)
sample = np.sort(np.mod(rng.normal(0,100, size=OBSERVATIONS), 2*np.pi))

# These points are places on the ellipse.
(X, Y) = e(sample)

# But our telescope is imperfectly calibrated.
# So, maybe we didn't measure a point EXACTLY on the ellipse,
#   Therefore, we bump the points off of the ellipse.
bumpX = 0.15*(2*rng.random(size=OBSERVATIONS)-1)
bumpY = 0.15*(2*rng.random(size=OBSERVATIONS)-1)
# Also, we our scope doesn't have infinite precision,
# We have some uncertainty in our observations.
#   So, we make up uncertainties
eX = 0.2*rng.normal(0.15, 0.05, size=OBSERVATIONS)
eY = 0.2*rng.normal(0.15, 0.05, size=OBSERVATIONS)
#   The correlation can be between -1 and +1
corr = 2*(rng.uniform(size=OBSERVATIONS)-0.5)
#   Note: these are not 'realistic' uncertainties that you'd get if you
#         actually tried to determine an orbit with telescope observations!

# Finally, we generate our 'observations'.
XY = np.array([gv.gvar(
    [x+dx, y+dy], 
    [[ex,c*np.sqrt(ex*ey)],[c*np.sqrt(ex*ey),ey]])
    for x, dx, ex, y, dy, ey, c in zip(X, bumpX, eX, Y, bumpY, eY, corr)])

X, Y = XY.transpose()

# To fit, we must make up priors.
# You can ballpark them by looking at the data,
# set the following to True
if False: 
    fig, ax = plt.subplots(1,1,squeeze=False)
    gvarplot.ellipses(ax[0][0], X, Y, color='black')
    ax[0][0].set_xlim(underlying['x0'] + underlying['a'] * np.array([-2, 2]))
    ax[0][0].set_ylim(underlying['y0'] + underlying['b'] * np.array([-2, 2]))
    ax[0][0].set_aspect(1)
    plt.show()
    exit()

priors = {
    'x0': gv.gvar('10(3)'),
    'y0': gv.gvar('12(2)'),
    'phi': gv.gvar('0(0.78)'),

    # We prior a and b to be different to prevent a numerical instability.
    'log(a-b)':  gv.log(gv.gvar('2(2)')),
    'b':  gv.gvar('2(2)'),
}

# We're hoping to find the best-fit ellipse.
# We should think of both the X and Y points as input and 
# demand that they satisfy the constraint
#
#    [ (x-x0) * cos phi + (y-y0) * sin phi ]^2 / a^2
#  + [ (x-x0) * sin phi - (y-y0) * cos phi ]^2 / b^2
#  = 1")
#
# So... what do we take as the 'data' to fit?
# We should rewrite the constraint as a level curve
#
# g(x, y) =   [ (x-x0) * cos phi + (y-y0) * sin phi ]^2 / a^2
#           + [ (x-x0) * sin phi - (y-y0) * cos phi ]^2 / b^2
#           - 1
#
# and the ellipse is when g(x,y) = 0.
#
# So, our dependent data is exactly known:
# it's 0 for each independent data point,
# because that observation obeys the constraint!
# Therefore, take the approach of 
#   https://lsqfit.readthedocs.io/en/latest/overview.html#y-has-no-error-marginalization

# We give a very small uncertainty on the constraint
# to prevent numerical issues:
constraint = gv.gvar(['0(0.00001)'] * OBSERVATIONS)

# Also, our independent data---the observations---have errors.
# So we adopt the approach of 
#   https://lsqfit.readthedocs.io/en/latest/overview.html#x-has-errors 
# and put those data into the priors.
priors['X'] = X
priors['Y'] = Y

# Now our fit is independent-data free,
# in the sense that we put them in the priors instead.
# So we can build a very simple fit function that takes only parameters
# It implements the level curve g(x,y) for all (X,Y).

def g(p):
    dX = p['X'] - p['x0']
    dY = p['Y'] - p['y0']
    c = np.cos(p['phi'])
    s = np.sin(p['phi'])
    asq = (p['a-b']+p['b'])**2
    bsq = p['b']**2
    return (dX * c + dY * s)**2 / asq + (dX * s - dY * c)**2 / bsq - 1

# Now we are ready to do the fit.
# The 'data' are the constraint: all points are on the level curve.
# The priors are the parametric priors and the data.
# The function is the level curve function.
fit = lsf.nonlinear_fit(data=constraint, prior=priors, fcn=g)
# Store a in the fit, as some functions have an argument called a.
# Is there a way to show this in the formatted fit result?
# Like where a-b is shown, under the line of dashes.
fit.p['a'] = fit.p['a-b'] + fit.p['b']

print(fit)
print(f"Computed best-fit parameters:")
print(f"              a     {fit.p['a-b']+fit.p['b']}")

# Strip out the independent data from the result,
# they're not needed to visualize the best-fit ellipse.
result = {param: fit.p[param] for param in underlying}
result['a'] = fit.p['a']

# Now we would like to visualize the best-fit ellipse.
# That isn't so bad, just plug the fit results to get a new ellipse.

best_fit = ellipse(**result)
bf = best_fit(theta)

fig, ax = plt.subplots()

# First, plot the underlying ellipse
ax.plot(*exact, color='black', marker=',', label='Underlying')
# and the data we've fit
gvarplot.ellipses(ax, X, Y, color='black', label='Observations')

# We can visualize the best-fit ellipse by plotting the mean,
gvarplot.mean(ax, *bf, color='darkgreen', label='Best fit')
# But, we want to know the uncertainty.
gvarplot.errorband(ax, *bf, sigma=[1,2], alpha=1/160, color='green', zorder=-1)
# You might have to fiddle with the alpha ^
# to prevent it from being too dark.

ax.set_xlim(5, 15)
ax.set_ylim(9.5, 14.5)

ax.legend(loc='upper left')

fig.tight_layout()

print("\n\nComparison of fit with underlying reality.")
for param in underlying:
    print(f"{param:10} {underlying[param]:<4} {fit.p[param]:16} {gv.abs(underlying[param]-fit.p[param]):16}")

# Let's see how our uncertainties are correlated with one another.
fig, ax = gvarplot.uncertainty_matrix(result.values(), [k for k in result.keys()] )

plt.show()
