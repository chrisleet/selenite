from astropy.io import fits
import argparse
from glob import glob
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


# Plots a given order for each spectrum from a given epoch; 
# on click places a line, after two lines prints pixel range and wavelength 
# range.

def build_px_masks():

  #np.seterr(all='raise')

  # 0: Parse program arguments
  parser = argparse.ArgumentParser(description="helps build pixel mask")
  parser.add_argument("order", help="specify order to plot")
  args = parser.parse_args()

  # 1(a): Get spectrum names
  all_spectra_names = glob("/home/chrisleet/astronomy/data/fitspec/201*/*/HR*")

  # 1(b): Get bad spectra
  bad_spectra_f = open(("/home/chrisleet/astronomy/expres_pipeline/expres"
                        "/selenite/config/bad_spectra.txt"), "r")
  bad_spectra = []
  for line in bad_spectra_f:
    bad_spectra.append(line[:-1])

  # 1(c) Remove bad spectra from spectra names
  spectra_names = set(all_spectra_names) - set(bad_spectra)


  # Observed stats:
  peak_snr = 559.0

  # Tracked stats:
  good_spectra_no = 0
  spectra_no = 0
  l_cutoff_wv, r_cutoff_wv = 0, np.inf

  # 3: Plot each spectra.
  fig = plt.figure(facecolor="white")
  cmap = plt.get_cmap('Spectral')

  order = int(args.order)
  for fname in sorted(spectra_names):

    # 3(a): Open file
    f = fits.open(fname, do_not_scale_file=True)
    lin_x = f[1].data.wavelength[order]
    lin_y = f[1].data.spectrum[order]
    uncertainty = f[1].data.uncertainty[order]

    # 3(b) Filter out nan
    good_px = np.logical_not(np.isnan(lin_y))
    lin_x = lin_x[good_px]
    lin_y = lin_y[good_px]
    uncertainty = uncertainty[good_px]

    # 3(c) Generate px snrs
    snr = lin_y / uncertainty
    normed_snr = snr / np.max(snr)
    mean_blaze_peak_snr = np.mean(snr[1500:-1500])
    normed_mean_blaze_peak_snr = mean_blaze_peak_snr / peak_snr

    # 3(d) Plot spectrum snr
    # Option (a) Color by mean blaze peak snr
    color_by_mean_blaze_peak_snr = False
    if color_by_mean_blaze_peak_snr:
      plt.plot(lin_x, lin_y, color=cmap(normed_mean_blaze_peak_snr))
      plt.annotate(mean_blaze_peak_snr, xy=(lin_x[2000], lin_y[2000]))

    # Option (b) Color by mean blaze peak snr w/ cutoff, print # good spectra
    color_by_mean_blaze_peak_snr_cutoff = False
    snr_cutoff = 190 # 170 ok too! #110
    if color_by_mean_blaze_peak_snr_cutoff:
      spectra_no += 1
      if mean_blaze_peak_snr > snr_cutoff:
        plt.plot(lin_x, lin_y, color=cmap(normed_mean_blaze_peak_snr))
        plt.annotate(mean_blaze_peak_snr, xy=(lin_x[2000], lin_y[2000]))
        good_spectra_no += 1
      else:
        plt.plot(lin_x, lin_y, color="r")

    # Option (c) Color by mean blaze peak snr, exclude spectra below cutoff
    show_good_spectra = True
    if show_good_spectra:
       if mean_blaze_peak_snr > snr_cutoff:
        plt.plot(lin_x, lin_y, color=cmap(normed_mean_blaze_peak_snr))
        plt.annotate(mean_blaze_peak_snr, xy=(lin_x[2000], lin_y[2000]))

    # Option (d) Only show good spectra, color each px by snr
    color_px_by_snr = False
    if color_px_by_snr:
      if mean_blaze_peak_snr > snr_cutoff:
        l_cutoff, r_cutoff = -500, -1
        plt.plot(lin_x[l_cutoff:r_cutoff], lin_y[l_cutoff:r_cutoff], 
                    color=cmap(normed_mean_blaze_peak_snr))
        plt.scatter(lin_x[l_cutoff:r_cutoff], lin_y[l_cutoff:r_cutoff], 
                    color=cmap(normed_snr[l_cutoff:r_cutoff]))

    # Option (e) Only show good spectra, color each px by snr, color px below
    # cutoff red
    color_px_by_snr = False
    if color_px_by_snr:
      if mean_blaze_peak_snr > snr_cutoff:
        px_cutoff = 50
        l_cutoff, r_cutoff = -500, -1
        plt.plot(lin_x[l_cutoff:r_cutoff], lin_y[l_cutoff:r_cutoff], 
                    color=cmap(normed_mean_blaze_peak_snr))
        plt.scatter(lin_x[l_cutoff:r_cutoff], lin_y[l_cutoff:r_cutoff], 
                    color=cmap(normed_snr[l_cutoff:r_cutoff]))
        plt.scatter(lin_x[l_cutoff:r_cutoff][snr[l_cutoff:r_cutoff]<px_cutoff], 
                    lin_y[l_cutoff:r_cutoff][snr[l_cutoff:r_cutoff]<px_cutoff], 
                    color="r")
        print(snr[l_cutoff:r_cutoff])

    # Option (f) Plot uncertanties
    plot_uncertainites = False
    if plot_uncertainites:
      plt.plot(lin_x, uncertainty)
    
    # Option (g): Plot n point moving average of good spectra uncertainties
    N = 10
    plot_av_uncertainties = False
    if plot_av_uncertainties:
      smoothed_uncertainities = np.convolve(uncertainty, np.ones((N,))/N, 
                                            mode='valid')
      plt.plot(lin_x[int(N/2-1):-int(N/2)], smoothed_uncertainities)
      
    # Option (h) Plot gradients of smoothed uncertainities, draw line at first
    # wavelength where every spectra is < cutoff
    spectra_cutoff = 0.00015 #0.00005
    plot_gradients = False
    if plot_gradients:
      smoothed_uncertainities = np.convolve(uncertainty, np.ones((N,))/N, 
                                            mode='valid')
      smoothed_deltas = smoothed_uncertainities[:-1] - \
                        smoothed_uncertainities[1:]
      plt.plot(lin_x[int(N/2):-int(N/2)], smoothed_deltas)

      spec_l_cutoff_ind = np.argmax(smoothed_deltas < spectra_cutoff)
      spec_l_cutoff_wv = lin_x[int(N/2):-int(N/2)][spec_l_cutoff_ind]
      l_cutoff_wv = spec_l_cutoff_wv if spec_l_cutoff_wv > l_cutoff_wv \
                                     else l_cutoff_wv

      spec_r_cutoff_ind = np.argmax(np.flip(smoothed_deltas) > -spectra_cutoff)
      spec_r_cutoff_wv = np.flip(lin_x[int(N/2):-int(N/2)])[spec_r_cutoff_ind]
      r_cutoff_wv = spec_r_cutoff_wv if spec_r_cutoff_wv < r_cutoff_wv \
                                     else r_cutoff_wv
      

    f.close()

  # Option (b) Color by mean blaze peak snr w/ cutoff, print # good spectra
  if color_by_mean_blaze_peak_snr_cutoff:
    print("good spec", good_spectra_no, "/", spectra_no, \
          good_spectra_no/float(spectra_no) * 100, "%")

  # Option (h) Plot gradients of smoothed uncertainities, draw line at first
  # wavelength where every spectra is < cutoff
  if plot_gradients:
    plt.axvline(l_cutoff_wv, color="r")
    plt.axvline(r_cutoff_wv, color="b")
    print("l_cutoff_wv", l_cutoff_wv, "r_cutoff_wv", r_cutoff_wv)

  # Option (i) Print number of pixels between cutoff points
  print_pixels_between_cutoff_points = True
  if print_pixels_between_cutoff_points:

    px_between_cutoff_points = []

    order = int(args.order)
    for fname in sorted(spectra_names):

      f = fits.open(fname, do_not_scale_file=True)
      lin_x = f[1].data.wavelength[order]
      l_px = np.argmax(lin_x > l_cutoff_wv)
      r_px = np.argmax(lin_x > r_cutoff_wv) - 1
      px_between_cutoff_points.append(r_px - l_px)
      f.close()

    print(np.mean(px_between_cutoff_points))
    

  plt.show()

  

#  min_uncertainties = sorted(min_uncertainties)

#  print("max snr", np.max(av_snrs))
#  fig = plt.figure(facecolor="white")
#  plt.plot(np.linspace(0, 1, len(min_uncertainties)), min_uncertainties)
#  plt.show()

if __name__ == "__main__":
  build_px_masks()
    
    

