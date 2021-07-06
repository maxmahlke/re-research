from datetime import datetime
import os
import sys

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import figure_setup as fs

PATH_GFX = os.path.join(os.path.dirname(__file__), '../gfx/')

def hlines_demo(FORMAT):
    """Plot a randomly chosen matplotlib example to illustrate the default
    plot layout.

    Example adapted from
    https://matplotlib.org/stable/gallery/lines_bars_and_markers/vline_hline_demo.html

    Parameters
    ==========
    FORMAT : str
        File format to save the figure in.
    """
    fig, ax = plt.subplots()

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    t = np.arange(0.0, 5.0, 0.1)
    s = np.exp(-t) + np.sin(2 * np.pi * t) + 1
    nse = np.random.normal(0.0, 0.3, t.shape) * s

    ax.plot(t, s + nse, "^", c='black')
    ax.vlines(t, [0], s, color='black')
    # By using ``transform=ax.get_xaxis_transform()`` the y coordinates are scaled
    # such that 0 maps to the bottom of the axes and 1 to the top.
    ax.vlines([1, 2], 0, 1, transform=ax.get_xaxis_transform(), colors='r')
    ax.set(xlabel=("Time / s"), ylabel=("Triangles"))

    plt.tight_layout()
    fig.savefig(os.path.join(PATH_GFX, f"hlines_demo.{FORMAT}"))

def solution_space(FORMAT):
    """Plot solution space to demonstrate a square figure. This is an
    adapted matplotlib example, from

    https://matplotlib.org/stable/gallery/images_contours_and_fields/
    contours_in_optimization_demo.html

    Parameters
    ==========
    FORMAT : str
        File format to save the figure in.
    """
    fig, ax = plt.subplots(figsize=fs.figsize(aspect=1))

    # Set up survey vectors
    xvec = np.linspace(0.001, 4.0, 101)
    yvec = np.linspace(0.001, 4.0, 105)

    # Set up survey matrices.  Design disk loading and gear ratio.
    x1, x2 = np.meshgrid(xvec, yvec)

    # Evaluate some stuff to plot
    obj = x1**2 + x2**2 - 2*x1 - 2*x2 + 2
    g1 = -(3*x1 + x2 - 5.5)
    g2 = -(x1 + 2*x2 - 4.5)
    g3 = 0.8 + x1**-3 - x2

    cntr = ax.contour(x1, x2, obj, [0.01, 0.1, 0.5, 1, 2, 4, 8, 16],
                    colors='black')
    ax.clabel(cntr, fmt="%2.1f", use_clabeltext=True)

    cg1 = ax.contour(x1, x2, g1, [0], colors='sandybrown')
    cg2 = ax.contour(x1, x2, g2, [0], colors='orangered')
    cg3 = ax.contour(x1, x2, g3, [0], colors='mediumblue')

    ax.set(xlim=(0, 4), ylim=(0, 4), xlabel='x / AU', ylabel='y / AU')

    plt.tight_layout()
    fig.savefig(os.path.join(PATH_GFX, f"solution_space.{FORMAT}"))


def matplotlib_release_dates(FORMAT):
    """Plot matplotlib release dates to showcase a two-column figure.

    Example adapted from
    https://matplotlib.org/stable/gallery/lines_bars_and_markers/timeline.html

    Parameters
    ==========
    FORMAT : str
        File format to save the figure in.
    """
    fig, ax = plt.subplots(figsize=fs.figsize(width=1, aspect=2))

    # Read in the data
    data = pd.read_csv(os.path.join(PATH_GFX, "../data/release_dates.csv"))
    names = data.version
    dates = data.date

    # Convert date strings (e.g. 2014-10-18) to datetime
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]

    # Choose some nice levels
    levels = np.tile([-5, 5, -3, 3, -1, 1],
                    int(np.ceil(len(dates)/6)))[:len(dates)]

    ax.vlines(dates, 0, levels, color="tab:red")  # The vertical stems.
    ax.plot(dates, np.zeros_like(dates), "-o",
            color="k", markerfacecolor="w")  # Baseline and markers on it.

    # annotate lines
    for d, l, r in zip(dates, levels, names):
        ax.annotate(r, xy=(d, l),
                    xytext=(-3, np.sign(l)*3), textcoords="offset points",
                    horizontalalignment="right",
                    verticalalignment="bottom" if l > 0 else "top")

    # format xaxis with 4 month intervals
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    ax.yaxis.set_visible(False)

    plt.tight_layout()
    fig.savefig(os.path.join(PATH_GFX, f"matplotlib_release_dates.{FORMAT}"))

if __name__ == "__main__":

    # figure_name : figure_function
    FIGURE_FUNCTIONS = {
        "hlines_demo": hlines_demo,
        "solution_space": solution_space,
        "matplotlib_release_dates": matplotlib_release_dates,
    }

    if len(sys.argv) < 2:
        print("Provide a figure name to compile it. Choose from:")
        print(list(FIGURE_FUNCTIONS.keys()))
        sys.exit()

    # Get the format if it was specified on the command line
    if "--format" in sys.argv:
       idx = np.where(sys.argv == "--format")[0] + 1
       FORMAT = sys.argv[idx]
    else:
       FORMAT = "pgf"

    # Call the figure function
    if not "--all" in sys.argv:
        figure_name = sys.argv[1]
        FIGURE_FUNCTIONS[figure_name](FORMAT)
    else:
        for figure, function in FIGURE_FUNCTIONS.items():
            print(f"Compiling {figure}..")
            function(FORMAT)
