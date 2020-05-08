import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from itertools import cycle

def reset_plot_kwargs():
    global recent_color, recent_linestyle, recent_marker
    recent_color = None
    recent_linestyle = None
    recent_marker = None

    global offset, colors, linestyles, markers
    offset = 0
    colors = cycle(sns.color_palette())

    global linestyles
    linestyles = cycle(["-", "--", ":", "-."])

    global markers
    markers = cycle(['D', 'o', 'X', '*', '<', 'd', 'S', '>', 's', 'v'])

def markevery(*, n_points, n_markers=10):
    """disperse n_markers evenly amongst n_points in a plot"""
    global offset
    if n_points > n_markers:
        markevery = int(n_points / n_markers)
        to_return = (offset, markevery)
        # golden ratio trick
        offset = (offset + int(.61803398875 * markevery)) % markevery
        return to_return
    else:
        return 1

# TODO: allow to "use_previous_style" (ie. color, linestyle, marker)

def plot(data, *plot_args, color=None, linestyle=None, marker=None, **plot_kwargs):
    """plot data against x as a line with markers"""

    # Optionally use the most recent style variables
    global recent_color, recent_linestyle, recent_marker
    if color == "recent": color = recent_color
    if linestyle == "recent": linestyle = recent_linestyle
    if marker == "recent": marker = recent_marker

    # If a param was provided, don't churn the corresponding generator
    plot_kwargs["color"] = color or next(colors)
    plot_kwargs["linestyle"] = linestyle or next(linestyles)
    plot_kwargs["marker"] = marker or next(markers)

    # Update the most recently used style variables
    recent_color = plot_kwargs["color"]
    recent_linestyle = plot_kwargs["linestyle"]
    recent_marker = plot_kwargs["marker"]

    # This can be safely recomputed every time since there is no generator
    plot_kwargs["markevery"] = markevery(n_points=len(data))

    plt.plot(data, **plot_kwargs)

def plot_medians_and_ci(*, x=None, data, ci, axis=0, **plot_kwargs):
    """plot column-wise median of `data` and optional confidence interval"""
    medians = np.median(data, axis=axis)

    # This is utilized for example when plotting errsqs vs iteration
    if x is None:
        x = np.arange(len(medians))

    plot(x=x, data=medians, **plot_kwargs)

    if ci != 0:
        # Compute the boundaries of the middle ci% of the data
        lower_ci = np.percentile(data, 50-ci/2, axis=axis)
        upper_ci = np.percentile(data, 50+ci/2, axis=axis)

        # Use whatever color was used to plot the medians
        global recent_color
        plt.fill_between(x, lower_ci, upper_ci,
                         color=recent_color,
                         alpha=0.25)

