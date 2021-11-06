#!/usr/bin/env python3

import gvar as gv
import matplotlib.pyplot as plt

defaults = {
        'alpha': 0.2,
        }

def vspan(ax, x, sigma=[1], **kwargs):
    if not sigma:
        return
    ax.axvspan(x.mean-sigma[0]*x.sdev, x.mean+sigma[0]*x.sdev, **{**defaults,**kwargs})
    if 'label' in kwargs:
        del kwargs['label']
    vspan(ax, x, sigma[1:], **kwargs)

def hspan(ax, y, sigma=[1], **kwargs):
    if not sigma:
        return
    ax.axhspan(y.mean-sigma[0]*y.sdev, y.mean+sigma[0]*y.sdev, **{**defaults,**kwargs})
    if 'label' in kwargs:
        del kwargs['label']
    hspan(ax, y, sigma[1:], **kwargs)

