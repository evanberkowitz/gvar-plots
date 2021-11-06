
import gvar as gv
import matplotlib as plt
from gvarplot import ellipses

defaults = {
        'alpha': 0.2,
        }

def errorband(ax, x, y, sigma=[1,2,3], **kwargs):
    if isinstance(x[0], gv._gvarcore.GVar) and isinstance(y[0], gv._gvarcore.GVar):
        # We can do something smarter than drawing zillions of ellipses
        # to get an error band by considering the curve, and finding
        # the turning points of distance to the tangent.
        # But, for now, this hack suffices.
        ellipses(ax, x, y, sigma, **{**defaults, **kwargs})
        return

    for s in sigma:
        ax.fill_between(x,
                gv.mean(y)-s*gv.sdev(y),
                gv.mean(y)+s*gv.sdev(y),
                **{**defaults, **kwargs})
        if 'label' in kwargs:
            del kwargs['label']

