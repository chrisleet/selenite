import sys

import matplotlib.pyplot as plt
import numpy as np

from scipy.interpolate import interp1d
from scipy import interpolate

def align_spectra(shard_dict, wv_grid_shard_dict):

  # If no sharded file has been provided as a wavelength grid, select
  # a calibration file to use as a standard wavelength grid.
  if wv_grid_shard_dict is None:
    std_filename = next(iter(next(iter(shard_dict.values())).spectra.keys()))

  # For each shard
  for key, shard in shard_dict.items():

    # Align all spectra to that wavelength grid
    wv_grid = next(iter(wv_grid_shard_dict[key].spectra.values())).lin_x
    wv_grid_log_y = next(iter(wv_grid_shard_dict[key].spectra.values())).log_y
    align_shard(shard, wv_grid, wv_grid_log_y)

def align_shard(shard, wv_grid, wv_grid_log_y):


    # For each spectrum != std_filename in shard
    for filename, spectrum in shard.spectra.items():

        # TEST 0: Plot the science spectrum against the wv grid spectrum
        plot_science_spectra_against_wv_grid_spectrum = False
        if plot_science_spectra_against_wv_grid_spectrum:
            fig = plt.figure(facecolor="white")
            plt.plot(wv_grid, wv_grid_log_y, color="blue", label="wv_grid")
            plt.plot(spectrum.lin_x, spectrum.log_y, color="red", 
                     label="science_spectrum")
            plt.legend()
            plt.show()


        # 1) Fit a low-order polynomial x = X(lambda) to the points 
        # (lambda, x), where lambda is the
        # wavelength solutions and x the pixel position's of the shard.
        WVPX_POLY_DEG = 10
        px_x = np.arange(len(spectrum.lin_x))
        x_mean = np.mean(spectrum.lin_x)
        wvpx_no_mean_model = np.polyfit(spectrum.lin_x-x_mean, px_x, 
                                        deg=WVPX_POLY_DEG, full=True)
        wvpx_no_mean_f = np.poly1d(wvpx_no_mean_model[0])
        wvpx_f = lambda x: wvpx_no_mean_f(x - x_mean)

        # 1) (Test) Plot wavelength to pixel function against data
        show_wvpx_f = False

        if show_wvpx_f:
            fig = plt.figure(facecolor="white")
            plt.scatter(spectrum.lin_x, px_x, color="red")
            plt.plot(spectrum.lin_x, wvpx_f(spectrum.lin_x), color="green")
            plt.show()

        # 2) Calculate x' = X(LAMBDA) where LAMBDA is the reference grid of 
        # wavelength values.
        resampled_px = wvpx_f(wv_grid)

        # 3)  Generate a function mapping the current spectrum's pixels to its 
        # intensities
        pxI_f = interp1d(px_x, spectrum.log_y, kind=1, bounds_error=False, 
                         fill_value=0.0)

        # 3) (Test) Plot function against current spectrum
        show_pxI_f = False
 
        if show_pxI_f: 
            upsampled_px_x = np.arange(len(spectrum.lin_x) * 10) / 10.0
            fig = plt.figure(facecolor="white")
            plt.scatter(px_x, spectrum.log_y, color="red")
            plt.plot(upsampled_px_x, pxI_f(upsampled_px_x), color="blue",
                     zorder=1)
            plt.show()

        # 4) Calculate pxI_f(x') - the intensities associated with the 
        # resampled pixel values.
        resampled_log_y = pxI_f(resampled_px)

        if np.isnan(resampled_log_y).any():
            sys.stderr.write("Can't resample "+filename+"  w/ cubic splines\n")
            pxI_lin_f = interp1d(px_x, spectrum.log_y, kind=1, 
                                 bounds_error=False, fill_value=0.0)
            resampled_log_y = pxI_lin_f(resampled_px)

            if np.isnan(resampled_log_y).any():
                print("resampling spectrum 2 wv grid produced nan")


        # 4) (Test) Plot the resampled log_y values with their new wavelengths 
        #    against the old spectrum's values.
        show_resampled_spectrum = False

        if show_resampled_spectrum:
            fig = plt.figure(facecolor="white")
            plt.plot(spectrum.lin_x, spectrum.log_y, color="red")
            plt.plot(wv_grid, resampled_log_y, color="green")
            plt.show()

        # 5) Set the spectrum's lin_x and log_y to the resampled values
        spectrum.lin_x = np.copy(wv_grid)
        spectrum.log_y = np.copy(resampled_log_y)
        
        # 6) Clear the spectrum's px_no, and set shard px_no
        spectrum.px_no = None
        shard.px_no = len(spectrum.log_y)
    
        
                
        
