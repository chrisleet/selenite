import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

def plot_model(shards, model, pwv, x_units, show=False, is_paper_plot=False):

    """
    Plot telluric model against spectrum to be reduced.
    """
    
    if not show:
        return

    mpl.rcParams.update({'font.size': 16})

    print("PWV:{}".format(pwv))

    for shardloc, shard in shards.items():
        plot_shard_model(shard, model, x_units, is_paper_plot)

def plot_shard_model(shard, model, x_units, is_paper_plot):

    """
    Plot telluric model against spectrum to be reduced for shard.
    """

    spectrum = next(iter(shard.spectra.values())) #only one spectrum in shard

    fig = plt.figure(facecolor = 'white')
    if x_units == "wavelength":
        plt.plot(spectrum.lin_x, np.exp(spectrum.log_y), label='Science Spectrum', color='purple')
        #plt.plot(spectrum.lin_x, spectrum.div_lin_y, label='Divided Spectrum', color='green')
        plt.plot(spectrum.lin_x, spectrum.tel_lin_y, label='Model', color="blue")
    elif x_units == "pixels":
        plt.plot(np.exp(spectrum.log_y), label='Science Spectrum', color='purple')
        plt.plot(spectrum.div_lin_y, label='Divided Spectrum', color='green')
        plt.plot(spectrum.tel_lin_y, label='Model', color="blue")
    else:
        raise Exception("Plot model: x_units not recognized")

    if not is_paper_plot:
        plt.title("Order {} spectrum and telluric model".format(shard.order))
    plt.xlabel(r'$Wavelength,\ \lambda,\ (\AA)$')
    plt.ylabel(r'$Normalized\ Flux, I_\lambda$')
    plt.tight_layout()
    plt.legend()

    def onclick(event):
      if event.button == 3:
        # print("(%f wv, %f intens)" % (event.xdata, event.ydata))
        print("    - %f" % (event.xdata))

    cid = fig.canvas.mpl_connect('button_press_event', onclick) 

    plt.show()             
