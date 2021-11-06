import numpy as np
import pandas as pd
import gvar as gv

def errorbar(ax, x, y, sigma=[1], **kwargs):
    if isinstance(x, pd.Series):
        errorbar(ax, np.array(x), y, **kwargs)
        return
    elif isinstance(x[0], gv._gvarcore.GVar):
        A = np.array([a.mean for a in x])
        dA= np.array([a.sdev for a in x])
    else:
        A = np.array(x)
        dA= np.zeros(x.shape)

    if isinstance(y, pd.Series):
        errorbar(ax, x, np.array(y), **kwargs)
        return
    elif isinstance(y[0], gv._gvarcore.GVar):
        B = np.array([b.mean for b in y])
        dB= np.array([b.sdev for b in y])
    else:
        B = np.array(y)
        dB= np.zeros(y.shape)

    defaults = {
    }
    defaults.update(kwargs)
    
    for s in sigma:
        ax.errorbar(A, B, xerr = s*dA, yerr = s*dB, **defaults)

