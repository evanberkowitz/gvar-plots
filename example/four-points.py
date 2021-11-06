#!/usr/bin/env python3

import gvar  as gv
import numpy as np

import matplotlib.pyplot as plt
from gvarplot import ellipse, errorbar

def four_points():
    fig, ax = plt.subplots()
    ax.set_title("Four points")

    point = gv.gvar([1, 0.75], [[0.1**2, 0.0015], [0.0015, 0.02**2]])

    X = np.array([point[0], point[1],   point[0], point[1]])
    Y = np.array([point[1], point[0], 1/point[0], point[1]])
    # Invert to get anticorrelation    ^.
    COLOR = ['blue', 'red', 'green', 'purple']

    for x,y,color in zip(X,Y, COLOR):
        ellipse(ax, x, y, sigma=[1,2,3],   color=color)
        errorbar(ax, [x], [y], marker='o', color=color)

    ax.set_aspect(1)
    fig.tight_layout()

if __name__ == "__main__":
    four_points()

    plt.show()
