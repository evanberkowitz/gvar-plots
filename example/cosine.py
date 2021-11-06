#!/usr/bin/env python

import numpy as np
import pandas as pd
import gvar as gv

import matplotlib.pyplot as plt

from gvarplot import ellipses, errorbar, mean, hspan

def cosine(rng, time=np.arange(0, 2*np.pi, 0.2)):
    fig, ax = plt.subplots()
    ax.set_title("Cosine")
    
    xy = []

    for t in time:
        # Make up sdevs and covariance
        dt = 0.2*(rng.uniform()-0.5)
        dy = 0.2*(rng.uniform()-0.5)
        da = 0.25*rng.uniform()
        db = 0.25*rng.uniform()
        cv = (1-2*rng.uniform()) * da * db
        # Add correlated point to list
        xy+= [ gv.gvar([t, dy+np.cos(t+dt)], [[ da**2, cv], [cv, db**2]]) ]
    
    xy = np.array(xy).transpose()

    ax.plot(time, np.cos(time), color='black')
    ellipses(ax, *xy, label='Ellipses')
    errorbar(ax, *xy, label='Error bars', marker='o', linestyle=':')
    hspan(ax, np.mean(xy[1]), sigma=[1,2,3], color='gray', label='Mean')
    ax.set_xlim(-0.5, 7)
    ax.set_ylim(-2, 2)
    ax.legend(loc='lower right')
    fig.tight_layout()

if __name__ == '__main__':
    rng = np.random.default_rng(seed=7)

    cosine(rng)

    plt.show()

