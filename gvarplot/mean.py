
import numpy as np
import pandas as pd
import gvar as gv

def mean(ax, x, y, **kwargs):
    """ Plot central values of gvars.

    Args:
        ax: A matplotlib axis.
        x:  An array of gvars indicating x-values.
        y:  An array of corresponding gvars indicating y-values.
        **kwargs:  options accepted by matplotlib's `plot`. 
    """
    defaults = {
        #'zorder': 1,
    }
    defaults.update(kwargs)

    if isinstance(x, pd.Series):
        mean(ax, np.array(x), y, **kwargs)
        return
    elif isinstance(x[0], gv._gvarcore.GVar):
        X = gv.mean(x)
    else:
        X = x

    if isinstance(y, pd.Series):
        mean(ax, X, np.array(y), **kwargs)
    elif isinstance(y[0], gv._gvarcore.GVar):
        Y = gv.mean(y)
    else:
        Y = y

    ax.plot(X, Y, **kwargs)


