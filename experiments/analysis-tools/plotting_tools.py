import h5py
import numpy as np
import matplotlib.pyplot as plt



def plot_h5_2d(
    filename,
    dataset_key,
    gradient_axis=None,
    ax=None,
    title=None,
    xlim=None,
    ylim=None,
    xlabel='X',
    ylabel='Y',
    clabel='Value',
    grid_x=None,
    grid_y=None,
    yvals= None,
    
    **imshow_kwargs
):
    """
    Plot a 2D dataset from an HDF5 file on a specified Matplotlib Axes,
    with optional cropping, axis labels, and colorbar label.

    Parameters
    ----------
    filename : str
        Path to the .h5 file.
    dataset_key : str
        Key for the 2D dataset (e.g., 'SET4_2d').
    gradient_axis : int or None
        If not None, compute gradient along this axis before plotting.
    ax : matplotlib.axes.Axes or None
        If given, draw on this axis. If None, create a new figure.
    title : str, optional
        Title for the plot.
    xlim : tuple of float, optional
        (x_min, x_max) range to crop in x-direction.
    ylim : tuple of float, optional
        (y_min, y_max) range to crop in y-direction.
    xlabel : str
        Label for the x-axis.
    ylabel : str
        Label for the y-axis.
    clabel : str
        Label for the colorbar.
    imshow_kwargs : dict
        Additional keyword arguments passed to `imshow`.

    Returns
    -------
    im : matplotlib.image.AxesImage
        The image object created by imshow.
    """

    with h5py.File(filename, 'r') as f:
        data = f[dataset_key][()]
        x = f['sweepgates_x'][()]
        y = f['sweepgates_y'][()]

        xvals = np.linspace(x[0][1], x[0][2], data.shape[1])
        
        if yvals is None:
            yvals = np.linspace(y[0][1], y[0][2], data.shape[0])

        # Optional cropping
        if xlim is not None:
            x_mask = (xvals >= xlim[0]) & (xvals <= xlim[1])
            data = data[:, x_mask]
            xvals = xvals[x_mask]
        if ylim is not None:
            y_mask = (yvals >= ylim[0]) & (yvals <= ylim[1])
            data = data[y_mask, :]
            yvals = yvals[y_mask]

        extent = [xvals[0], xvals[-1], yvals[0], yvals[-1]]

        if gradient_axis is not None:
            data = np.gradient(data, axis=gradient_axis, edge_order = 2)

    if ax is None:
        fig, ax = plt.subplots()

    im = ax.imshow(data, extent=extent, origin='lower', aspect='auto', **imshow_kwargs)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)

    if ax.figure == plt.gcf():
        plt.colorbar(im, ax=ax, label=clabel)

    if grid_x:
        ax.set_xticks(np.arange(xlim[0] if xlim else xvals[0], xlim[1] if xlim else xvals[-1], grid_x))
        
    if grid_y:
        ax.set_yticks(np.arange(ylim[0] if ylim else yvals[0], ylim[1] if ylim else ifyvals[-1], grid_y))

    if grid_x or grid_y:
        ax.grid(color='w', linestyle='--', linewidth=1)
    return im