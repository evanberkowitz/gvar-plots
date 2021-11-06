

import gvar as gv
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def ellipse(ax, x, y, sigma=[1], **kwargs):
    """ Plot an error ellipse around a pair of gvars.

    Args:
        ax: A matplotlib axis.
        x:  A gvar indicating the x-value.
        y:  A gvar indicating the y-value.

        sigma: A list of standard deviations for which to draw an ellipse.
        **kwargs: options accepted by matplotlib.patches.Ellipse.  The default is alpha=0.2.
    """

    if (not isinstance(x, gv._gvarcore.GVar)) or (not isinstance(y, gv._gvarcore.GVar)):
        raise TypeError("GVars required for an error ellipse.")

    defaults = {
            'alpha': 0.2,
            }
    defaults.update(kwargs)

    C = gv.evalcov((x,y))
    w, v = np.linalg.eigh(C)
    w = np.sort(w)[::-1]

    if C[0,1] == 0 and C[0,0] >= C[1,1]:
        angle = 0
    elif C[0,1] == 0 and C[0,0] < C[1,1]:
        angle = np.pi/2
    else:
        angle = np.arctan2(w[0]-C[0,0], C[0,1])
    
    # matplotlib wants angle in degrees
    angle = angle*180/np.pi

    for s in sigma:
        # mpl.patches.Ellipse wants full axes, not semi-{minor,major} axes.
        axes = 2*s*np.sqrt(w) # ... hence the 2*.
        e = patches.Ellipse([x.mean, y.mean], *axes, angle=angle, **defaults)
        ax.add_patch(e)

def ellipses(ax, x, y, sigma=[1], **kwargs):
    """ Plot error ellipses around arrays of gvars.

    Args:
        ax: A matplotlib axis.
        x:  An array of gvars indicating the x-value on which to center ellipses.
        y:  An array of corresponding gvars indicating the y-values on which to center the ellipses.
        sigma: A list of standard deviations for which to draw an ellipse for each (`x`, `y`) pair.
        **kwargs: options accepted by `matplotlib.patches.Ellipse`.  The default `alpha=0.2`.

    The correlation between `x` and `y` is used to determine the corresponding error ellipse.
    """

    defaults = dict(kwargs)

    if 'label' not in defaults:
        for a, b in zip(x, y):
            ellipse(ax, a, b, sigma=sigma, **defaults)
    else:
        ellipse(ax, x[0], y[0], sigma=sigma, **defaults)
        del defaults['label']
        for a, b in zip(x[1:], y[1:]):
            ellipse(ax, a, b, sigma=sigma, **defaults)

