import numpy as np

def find_uncertainty_cutoffs(shard_dict, config):

  for order, shard in shard_dict.items():

    l_cutoff_wv, r_cutoff_wv = 0, np.inf
    for spectrum in shard.spectra.values():
 
      # 1: Get n point moving average of uncertainties
      N = 10
      smoothed_uncertainty = np.convolve(spectrum.uncertainty, np.ones((N,))/N,  
                                         mode='valid')
        
      # 2: Get smoothed uncertainities gradient
      # wavelength where every spectra is < cutoff
      smoothed_deltas = smoothed_uncertainty[:-1] - smoothed_uncertainty[1:]
      lin_x_truncated = spectrum.lin_x[int(N/2):-int(N/2)]

      # 3: Find the first wavelength that the spectrum's uncertainty falls 
      # below the gradient_cutoff on the left and on the right. If this is 
      # greater/smaller than the current gradient cutoff, update the 
      # gradient cutoff   
      gradient_cutoff = float(config["b_star_uncertainity_gradient_cutoff"])
      spc_l_cutoff_ind = np.argmax(smoothed_deltas < gradient_cutoff)
      spc_l_cutoff_wv = lin_x_truncated[spc_l_cutoff_ind]
      l_cutoff_wv = spc_l_cutoff_wv if spc_l_cutoff_wv > l_cutoff_wv \
                                    else l_cutoff_wv

      spc_r_cutoff_ind = np.argmax(np.flip(smoothed_deltas)>-gradient_cutoff)
      spc_r_cutoff_wv = np.flip(lin_x_truncated)[spc_r_cutoff_ind]
      r_cutoff_wv = spc_r_cutoff_wv if spc_r_cutoff_wv < r_cutoff_wv \
                                    else r_cutoff_wv

    # 4: Store order gradient cutoffs
    shard.l_cutoff_wv = l_cutoff_wv
    shard.r_cutoff_wv = r_cutoff_wv

def remove_fringes(shard_dict):

    for order, shard in shard_dict.items():

      for spectrum in shard.spectra.values():

        l_cutoff_px = np.argmax(spectrum.lin_x > shard.l_cutoff_wv) - 1
        r_cutoff_px = np.argmax(spectrum.lin_x > shard.r_cutoff_wv)
        #print("l_cutoff_px", l_cutoff_px, "r_cutoff_px", r_cutoff_px)

        spectrum.lin_x = spectrum.lin_x[l_cutoff_px:r_cutoff_px+1]
        spectrum.log_y = spectrum.log_y[l_cutoff_px:r_cutoff_px+1]
        spectrum.continuum = spectrum.continuum[l_cutoff_px:r_cutoff_px+1]
        spectrum.uncertainty = spectrum.uncertainty[l_cutoff_px:r_cutoff_px+1]
        spectrum.snrs = spectrum.snrs[l_cutoff_px:r_cutoff_px+1]
        spectrum.px_no = len(spectrum.log_y)
  
    

    
    
