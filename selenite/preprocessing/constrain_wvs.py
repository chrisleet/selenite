import matplotlib.pyplot as plt
import numpy as np

def constrain_science_spectrum_wvs(shard_dict, order_wv_ranges):

  for order, shard in shard_dict.items():
    l_cutoff_wv, r_cutoff_wv = order_wv_ranges[order]

    spectrum = next(iter(shard.spectra.values()))

    constrain_spectrum(spectrum, l_cutoff_wv, r_cutoff_wv)

def constrain_wv_grid_wvs(shard_dict, wv_grid_shard_dict):
  
  for order, shard in shard_dict.items():
    if order in wv_grid_shard_dict:
    
      spectrum = next(iter(wv_grid_shard_dict[order].spectra.values()))

      constrain_spectrum(spectrum, shard.l_cutoff_wv, shard.r_cutoff_wv)
     
      should_check_constraints = False
      if should_check_constraints:
        check_constraints(shard_dict, wv_grid_shard_dict, order)

def constrain_spectrum(spectrum, l_cutoff_wv, r_cutoff_wv):

  l_cutoff_px = np.argmax(spectrum.lin_x > l_cutoff_wv)
  r_cutoff_px = np.argmax(spectrum.lin_x > r_cutoff_wv)
  if r_cutoff_px == 0:
    r_cutoff_px = -1

  spectrum.lin_x = spectrum.lin_x[l_cutoff_px:r_cutoff_px]
  spectrum.log_y = spectrum.log_y[l_cutoff_px:r_cutoff_px]
  spectrum.continuum = spectrum.continuum[l_cutoff_px:r_cutoff_px]
  spectrum.uncertainty = spectrum.uncertainty[l_cutoff_px:r_cutoff_px]
  spectrum.snrs = spectrum.snrs[l_cutoff_px:r_cutoff_px]
    

def check_constraints(shard_dict, wv_grid_shard_dict, order):

  fig = plt.figure(facecolor="white")   
  for bstar_spectrum in shard_dict[order].spectra.values():
    plt.plot(bstar_spectrum.lin_x, bstar_spectrum.log_y, color="blue")

  sci_spectrum = next(iter(wv_grid_shard_dict[order].spectra.values()))
  plt.plot(sci_spectrum.lin_x, sci_spectrum.log_y, color="orange")

  plt.axvline(shard_dict[order].l_cutoff_wv)
  plt.axvline(shard_dict[order].r_cutoff_wv)

  plt.title("Constrained b stars order {}".format(order))
  plt.xlabel("Wavelength (A)")
  plt.ylabel("Signal intensity")

  plt.show()
  

