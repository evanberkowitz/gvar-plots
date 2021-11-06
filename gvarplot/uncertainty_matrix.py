#!/usr/bin/env python3

import gvar as gv
import matplotlib.pyplot as plt
from gvarplot import ellipse, mean, hspan, vspan

def uncertainty_matrix(gvs, labels=None, sigma=[1,2,3], **kwargs):

    if isinstance(gvs, dict) or isinstance(gvs, gv._gvarcore.BufferDict):
        keys = [k for k in gvs]
        fig, ax = uncertainty_matrix(
                [gvs[k] for k in keys],
                labels=keys if not labels else labels,
                sigma=sigma, **kwargs)
        return fig, ax

    if isinstance(labels, str):
        labels=[f"{labels}{n}" for n in range(len(gvs))]

    fig, ax = plt.subplots(
            len(gvs), len(gvs),
            sharex='col', sharey='row',
            squeeze=False)

    default = {
            'color': 'blue',
            }

    default.update(kwargs)

    max_dev = max([v.sdev for v in gvs])
    diff = 1.1*max(sigma)*max_dev

    for i,x in enumerate(gvs):
        for j,y in enumerate(gvs):
            ellipse(ax[j][i], x, y, sigma=sigma, **default)
            ax[j][i].axhline(y.mean, linewidth=0.5, **default)
            ax[j][i].axvline(x.mean, linewidth=0.5, **default)
            ax[j][i].set_xlim((x.mean-diff, x.mean+diff))
            ax[j][i].set_ylim((y.mean-diff, y.mean+diff))
            ax[j][i].set_aspect('equal')

            if i==j:
                vspan(ax[j][i], x, sigma=sigma, **default)
                hspan(ax[j][i], y, sigma=sigma, **default)

        if labels:
            ax[0][i].set_title(labels[i])
            ax[i][0].set_ylabel(labels[i])
            ax[-1][i].tick_params(axis='x', labelrotation=45)

    return fig, ax
