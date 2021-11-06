import numpy as np
import pandas as pd
import gvar as gv

def errorbar(ax, x, y, **kwargs):
    if isinstance(x, pd.Series):
        errorbar(ax, np.array(x), y, **kwargs)
        return
    elif isinstance(x[0], gv._gvarcore.GVar):
        A = [a.mean for a in x]
        dA= [a.sdev for a in x]
    else:
        A = x
        dA= np.zeros(x.shape)

    if isinstance(y, pd.Series):
        errorbar(ax, x, np.array(y), **kwargs)
        return
    elif isinstance(y[0], gv._gvarcore.GVar):
        B = [b.mean for b in y]
        dB= [b.sdev for b in y]
    else:
        B = y
        dB= np.zeros(y.shape)

    defaults = {
    }
    defaults.update(kwargs)
    
    ax.errorbar(A, B, xerr = dA, yerr = dB, **defaults)

