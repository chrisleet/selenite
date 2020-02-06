import matplotlib.pyplot as plt
import numpy as np

from load_store import db_indicies as dbi

def plot_data(shard_dict, x_units, y_scale, show=False, append_to_title=""):
    
    """
    Plot each shard in the shard dict.

    Parameters
    ----------
    shards: dict
        Dictionary containing shards

    x_units: str
       Specifies whether to plot x-axis in pixels or angstroms

    y_scale: str
       Specifies whether to plot y-axis in lin space or log space

    show: bool
       Flag specifying whether to suppress the plot.

    append_to_title: str
       String to append to plot title.
    """

    if not show:
        return

    for shard in shard_dict.values():
        plot_shard_data(shard, y_scale, x_units, append_to_title)


def plot_shard_data(shard, y_scale, x_units, append_to_title):

    line_plot = True # Toggle between line plot and scatter plot

    fig = plt.figure(facecolor='white')
    plt.title(("Order:{} spectra in {} space {}" 
               " ").format(shard.order, y_scale, append_to_title))
        
    for spectrum_name, spectrum in shard.spectra.items():

        print("spectrum.log_y", np.exp(spectrum.log_y))
        print("len(spectrum.log_y)", len(np.exp(spectrum.log_y)))

        if x_units == "px":
            plt.xlabel("Pixels (Arbitrary 0)")
            if y_scale == "lin":
                if line_plot:
                    # x: pixels, y: linear space, line plot
                    plt.plot(np.exp(spectrum.log_y), label=spectrum_name)
                else: # (scatter plot)
                    # x: pixels, y: linear space, scatter plot
                    plt.scatter(list(range(shard.px_no)), np.exp(spectrum.log_y))
                plt.ylabel("Signal Intensity (linear space)")
            else: # (log plot)
                if line_plot:
                    # x: pixels, y: log space, line plot
                    plt.plot(spectrum.log_y, label=spectrum_name)
                else:
                    # x: pixels, y: log space, scatter plot
                    plt.scatter(list(range(shard.px_no)), spectrum.log_y)
                plt.ylabel("Signal Intensity (log space)")

        elif x_units == "wv":
            plt.xlabel("Wavelength (Angstroms)")
            if y_scale == "lin":
                if line_plot:
                    # x: wavelength, y: linear space, line plot
                    plt.plot(spectrum.lin_x, np.exp(spectrum.log_y))
                else: # (scatter plot)
                    # x: wavelength, y: linear space, scatter plot
                    plt.scatter(spectrum.lin_x, np.exp(spectrum.log_y))
                plt.ylabel("Signal Intensity (linear space)")
            else: # (log plot)
                if line_plot:
                    # x: wavelength, y: log space, line plot
                    plt.plot(spectrum.lin_x, spectrum.log_y)
                else:
                    # x: wavelength, y: log space, scatter plot
                    plt.scatter(spectrum.lin_x, spectrum.log_y)
                plt.ylabel("Signal Intensity (log space)")

        else:
            raise Exception("xUnits unrecognized when plotting shards")

    plt.show()



        

def plot_shards_vs_xcorr_tel(db, shift, shards, show=False):

    """
    Plots each shard against the xcorrelated, unfitted telluric model.
    """

    if not show:
        return

    for shard in shards.values():
        plot_shard_vs_xcorr_tel(db, shift, shard)

def plot_shard_vs_xcorr_tel(db, shift, shard):
    
    """
    Plots a shard against the xcorrelated, unfitted telluric model.

    Worker function of plot_shards_vs_xcorr_tel.
    """

    spectrum = next(iter(shard.spectra.values())) #only one spectrum in shard

    db_spectrum = np.ones(len(spectrum.log_y))
    for record in db:
        px = record[dbi.PX_IND] + shift
        if record[dbi.ORD_IND] == shard.order and shard.lo_px <= px and px < shard.hi_px:
            db_spectrum[px - shard.lo_px] = np.exp(record[dbi.INT_IND])

    fig = plt.figure(facecolor = 'white')
    plt.plot(spectrum.lin_x, np.exp(spectrum.log_y), color='purple', label='CHIRON Spectrum')
    plt.plot(spectrum.lin_x, db_spectrum, label='Telluric Spectrum')
    plt.title("Order {} px {}-{}, spectrum and xcorr, unscaled telluric model".format(shard.order, 
                                                                                     shard.lo_px,
                                                                                     shard.hi_px))
    plt.xlabel("Wavelength (Angstroms)")
    plt.ylabel("Signal strength")
    plt.tight_layout()
    plt.legend()
    plt.show()
    
