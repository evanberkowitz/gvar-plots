#!/usr/bin/env python3

import gvar as gv
import matplotlib.pyplot as plt

defaults = {
        'alpha': 0.2,
        }

def vspan(ax, x, sigma=[1], **kwargs):
    if 'label' not in kwargs:
        for s in sigma:
            ax.axvspan(x.mean-s*x.sdev, x.mean+s*x.sdev, **{**defaults,**kwargs})
    else:
        ax.axvspan(x.mean-sigma[0]*x.sdev, x.mean+sigma[0]*x.sdev, **{**defaults,**kwargs})
        del kwargs['label']
        for s in sigma[1:]:
            ax.axvspan(x.mean-s*x.sdev, x.mean+s*x.sdev, **{**defaults,**kwargs})

def hspan(ax, y, sigma=[1], **kwargs):
    if 'label' not in kwargs:
        for s in sigma:
            ax.axhspan(y.mean-s*y.sdev, y.mean+s*y.sdev, **{**defaults,**kwargs})
    else:
        ax.axhspan(y.mean-sigma[0]*y.sdev, y.mean+sigma[0]*y.sdev, **{**defaults,**kwargs})
        del kwargs['label']
        for s in sigma:
            ax.axhspan(y.mean-s*y.sdev, y.mean+s*y.sdev, **{**defaults,**kwargs})

