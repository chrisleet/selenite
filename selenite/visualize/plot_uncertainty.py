import matplotlib.pyplot as plt
import numpy as np

from expres.selenite.preprocessing.filter_bstars import B_PEAK_ST, B_PEAK_END

def plot_bstar_snrs(shard_dict, config, show=False):

  if not show:
    return

  cmap = plt.get_cmap('Spectral')

  for order, shard in shard_dict.items():

    good_spectra_no = 0
    spectra_no = 0

    # 1: Find maximum mean blaze peak SNR 
    max_peak_snr = 0
    for fname, spectrum in shard.spectra.items():
      blaze_peak_snr = np.mean(spectrum.snrs[B_PEAK_ST:B_PEAK_END])
      if blaze_peak_snr > max_peak_snr:
        max_peak_snr = blaze_peak_snr

    print(max_peak_snr)

    # 2: Plot each spectrum colored by and annotated with its SNR
    fig = plt.figure(facecolor="white")
    for fname, spectrum in shard.spectra.items():
      
      # 2(a): Get spectrum mean blaze peak SNR and norm it
      blaze_peak_snr = np.mean(spectrum.snrs[B_PEAK_ST:B_PEAK_END])
      #print(blaze_peak_snr)
      normed_peak_snr = blaze_peak_snr/max_peak_snr

      # 2(b): If spectra blaze peak snr > cutoff, color spectra by its snr
      #       and increment good spectra
      mid_px = int(len(spectrum.lin_x) / 2)
      cutoff_snr = float(config["b_star_SNR_cutoff"])
      if order > 81:
        cutoff_snr = float(config["high_order_b_star_SNR_cutoff"])

      if blaze_peak_snr > cutoff_snr:
        plt.plot(spectrum.lin_x, np.exp(spectrum.log_y), 
                 color=cmap(normed_peak_snr))
        plt.annotate(blaze_peak_snr, xy=(spectrum.lin_x[mid_px], 
                                         np.exp(spectrum.log_y)[mid_px]))
        good_spectra_no += 1

      # 2(c): Otherwise, color spectra red
      else:
        plt.plot(spectrum.lin_x, np.exp(spectrum.log_y), color="r")
        plt.annotate(blaze_peak_snr, xy=(spectrum.lin_x[mid_px], 
                                         np.exp(spectrum.log_y)[mid_px]))

      #if blaze_peak_snr < 100:
      #  print(fname, blaze_peak_snr)

      spectra_no += 1
    
    # 3: Print out the number and percent of good spectra
    print("Good spectra:", good_spectra_no, "/", spectra_no, \
          good_spectra_no/float(spectra_no) * 100, "%")

    # 4: Generate plot
    plt.show()

def plot_uncertainty_cutoffs(shard_dict, show=False):

  if not show:
    return

  for order, shard in shard_dict.items():

    fig = plt.figure(facecolor="white")
    for spectrum in shard.spectra.values():
    
      # 1: Plot uncertanty
      plot_uncertainty = True
      if plot_uncertainty:
        plt.plot(spectrum.lin_x, spectrum.uncertainty)
      
      # 2: Plot n point moving average of uncertainties
      N = 10
      plot_av_uncertainty = True
      if plot_av_uncertainty:
        smoothed_uncertainty = np.convolve(spectrum.uncertainty, 
                                           np.ones((N,))/N,  mode='valid')
        plt.plot(spectrum.lin_x[int(N/2-1):-int(N/2)], smoothed_uncertainty)
        
      # 3: Plot gradients of smoothed uncertainities, draw line at first
      # wavelength where every spectra is < cutoff
      plot_gradients = True
      if plot_gradients:
        smoothed_uncertainty = np.convolve(spectrum.uncertainty, 
                                           np.ones((N,))/N, mode='valid')
        smoothed_deltas = smoothed_uncertainty[:-1] - smoothed_uncertainty[1:]
        lin_x_truncated = spectrum.lin_x[int(N/2):-int(N/2)]
        plt.plot(lin_x_truncated, smoothed_deltas)


    # 4: Draw lines to show the cutoff wavelengths
    if plot_gradients:
      plt.axvline(shard.l_cutoff_wv, color="r")
      plt.axvline(shard.r_cutoff_wv, color="b")

    # 5: Print number of pixels between cutoff wavelengths
    print_pixels_between_cutoff_points = True
    if plot_gradients and print_pixels_between_cutoff_points:

      px_between_cutoff_wv = []

      for spectrum in shard.spectra.values():

        l_px = np.argmax(spectrum.lin_x > shard.l_cutoff_wv)
        r_px = np.argmax(spectrum.lin_x > shard.r_cutoff_wv) - 1
        px_between_cutoff_wv.append(r_px - l_px)

      print("order", order, "px between cutoff wavelengths", 
            np.mean(px_between_cutoff_wv))

    plt.xlabel("Wavelength (Angstroms)")
    plt.ylabel("Uncertainty")
    plt.title("Order {} uncertainties and cutoff wavelengths".format(order))
    plt.show()

def plot_bstar_cutoffs(shard_dict, show=False):

  if not show:
    return

  for order, shard in shard_dict.items():

    fig = plt.figure(facecolor="white")
    for spectrum in shard.spectra.values():
      plt.plot(spectrum.lin_x, np.exp(spectrum.log_y))  
    plt.axvline(shard.l_cutoff_wv, color="r")
    plt.axvline(shard.r_cutoff_wv, color="b")
      
    plt.xlabel("Wavelength (Angstroms)")
    plt.ylabel("Signal strength")
    plt.title("Order {} raw data with wavelength cutoffs".format(order))
    plt.show()
    
    
