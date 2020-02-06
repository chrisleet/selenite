import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os

from astropy.io import fits

from expres.selenite.load_store import load_fits

def plot_tellurics():

    mpl.rcParams.update({'font.size': 16})

    # 1: Read command line arguments
    parser = argparse.ArgumentParser(description="plots the flagged pixels in a fits file")
    parser.add_argument("spectrum_path", metavar="spectrum (*.fits)",
                        help="path to spectrum to plot")
    parser.add_argument("-o", "--order", help="specify order to plot")
    args = parser.parse_args()

    # 2: Load spectrum, choose orders to plot
    f = fits.open(args.spectrum_path, do_not_scale_image_data=True)
    if args.order is not None:
        orders = [int(args.order)]
    else:
        orders = list(range(38,82))

     # 3: Determine file type
    for order in orders:
        lin_x = f[1].data.wavelength[order]
        lin_y = f[1].data.spectrum[order] / f[1].data.continuum[order]
        tel = f[1].data.tellurics[order]

        plt.plot(lin_x, lin_y, color="k", label="EXPRES Spectrum")
        plt.plot(lin_x, tel, color="b", label="Telluric model")

    plt.xlabel(r'$Wavelength,\ \lambda,\ (\AA)$')
    plt.ylabel(r'$Normalized\ Flux, I_\lambda$')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    plot_tellurics()
