import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from load_store import db_indicies as dbi

def plot_shard_property(shard, calibrators, property, x_units, calibrator_px):

    """
    Plot the given shard with each spectrum colored by property.

    Parameters
    ----------
    shards: dict
        Dictionary containing shards

    calibrators: tuple
        Contains a list of spectra and their airmass and PWV

    property: {airmass, PWV}
       String specifying which property to color spectra by

    x_units: {pixels, wavelength}
       Specifies whether to plot x-axis in pixels or wavelength
    """

    # 1: Choose property to color spectra by
    w_calibrator, z_calibrator, f_order = calibrators
    #print("property:{}".format(property))
    if property == "PWV":
        property_list = np.array(w_calibrator)
        cmap_type = 'Spectral'
    elif property == "PWV_out":
        property_list = np.abs(np.array(w_calibrator))
        cmap_type = 'Spectral_r'
    elif property == "z":
        property_list = np.array(z_calibrator)
        cmap_type = 'Spectral'
    else:
        raise Exception("Did not recognize property to plot")

    # 2: Generate title
    title = ("Order:{} spectra in log space colored by {}").format(shard.order,
                                                                   property)

    # 3: Generate plot colors
    cmap = plt.get_cmap('Spectral')
    lo_p, hi_p = np.min(property_list), np.max(property_list)
    colors = (property_list - lo_p) / float(hi_p - lo_p)
    color_range = mpl.colors.Normalize(vmin=lo_p, vmax=hi_p)
    
    # 4: Set up plot & generate colorbar
    fig = plt.figure(facecolor='white')
    fig.suptitle(title)
    ax_cb = fig.add_axes([0.85, 0.10, 0.05, 0.83])
    cb = mpl.colorbar.ColorbarBase(ax_cb, cmap=cmap, norm=color_range)

    if property == "PWV":
        cb.set_label("Average water cal line depth")
    elif property == "PWV_out":
        cb.set_label("CRYSTAL PWV Metric")
    elif property == "z":
        cb.set_label("Airmass, z")
    else:
        raise Exception("Did not recognize property to plot")
    
    # 5: Generate plot
    ax_plt = fig.add_axes([0.12, 0.10, 0.68, 0.83])
    plt.ylabel("Signal Intensity (log space)")
    for filename, color in zip(f_order, colors):

        if filename not in shard.spectra:
          continue

        spectrum = shard.spectra[filename]

        if x_units == "pixels":
            plt.xlabel("Pixels (Arbitrary 0)")
            plt.plot(spectrum.log_y, label=filename, color=cmap(color), zorder=1)
        elif x_units == "wavelength":
            plt.xlabel("Wavelength (Angstroms)")
            plt.plot(spectrum.lin_x, spectrum.log_y, label=filename, color=cmap(color), zorder=1)
        else:
            raise Exception("xUnits unrecognized when plotting shard property")

        # 6: If property == PWV, plot any PWV calibration pixels
        if property == "PWV":
            for order, px in calibrator_px:
                if order == shard.order:
                    plt.scatter(spectrum.lin_x[px], spectrum.log_y[px], color="blue", zorder=2)

    # 7: Setup rightclicks
    def onclick(event):
        if event.button == 3:
            print("    - %f" % (event.xdata))

    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    # 8: Publish plot
    plt.show()


def plot_property(shards, calibrators, property, x_units, calibrator_px, show):
    
    """
    Plot each shard in the shard dict colored by property.

    Parameters
    ----------
    shards: dict
        Dictionary containing shards

    calibrators: tuple
        Contains a list of spectra and their airmass and PWV

    property: {airmass, PWV}
       String specifying which property to color spectra by

    x_units: {pixels, wavelength}
       Specifies whether to plot x-axis in pixels or wavelength

    show: bool
       Flag specifying whether to suppress the plot.
    """

    if not show:
        return

    for shard in shards.values():
        plot_shard_property(shard, calibrators, property, x_units, calibrator_px)
        
