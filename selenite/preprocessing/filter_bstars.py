import numpy as np

# Globals
B_PEAK_ST, B_PEAK_END = 1500, -1500


# Filters out low SNR b stars
def filter_lo_snr_bstars(shard_dict, config):
  
  for order, shard in shard_dict.items():

    low_snr_spectra = []

    cutoff_snr = float(config["b_star_SNR_cutoff"])
    if order > 82:
      cutoff_snr = float(config["high_order_b_star_SNR_cutoff"])

    for fname, spectrum in shard.spectra.items():
      
      # 1: Get spectrum mean blaze peak SNR
      blaze_peak_snr = np.mean(spectrum.snrs[B_PEAK_ST:B_PEAK_END])

      # 2: If spectrum's mean blaze peak SNR is < cutoff, add fname to 
      #       load_snr_spectra
      if blaze_peak_snr < cutoff_snr:
        low_snr_spectra.append(fname)

    # 3: Delete low_snr_spectra
    for fname in low_snr_spectra:
      del shard.spectra[fname]


def filter_bstars_with_unflatted_stellar_lines(shard_dict):
  
  filter_regions =  {38 : [[5018.2, 5018.4, 0.02, "gt"],
                           [5018.2, 5018.4, -0.02, "lt"],
                           [5015.8, 5016.5, -0.02, "lt"],
                           [5019.0, 5020.5, -0.02, "lt"],
                           [5020.8, 5021.0, -0.02, "lt"]],

                     39 : [[5056.6, 5056.7, -0.02, "lt"], 
                           [5043.1, 5043.2, -0.03, "lt"],
                           [5042.3, 5042.7, -0.02, "lt"], 
                           [5045.2, 5045.3, -0.02, "lt"]],

                     40 : [[5076.1, 5076.2, -0.03, "lt"],
                           [5117.6, 5117.8, -0.02, "lt"]],

                     41 : [[5168.0, 5168.5, -0.04, "lt"], 
                           [5133.6, 5134.0, 0.02, "gt"],
                           [5173.0, 5174.2, -0.04, "lt"], 
                           [5168.0, 5169.0, -0.03, "lt"]],

                     42 : [[5170.4, 5170.7, -0.025, "lt"],
                           [5170.4, 5170.7, 0.015, "gt"],
                           [5169.5, 5171.0, -0.025, "lt"],
                           [5169.5, 5171.0, 0.015, "gt"],
                           [5204.0, 5204.5, 0.02, "gt"]],

                    43 : [[5227.0, 5229.0, -0.02, "lt"],
                          [5251.6, 5251.7, -0.02, "lt"],
                          [5249.4, 5249.8, -0.02, "lt"],
                          [5249.4, 5249.8, 0.01, "gt"],
                          [5248.9, 5249.0, -0.02, "lt"],
                          [5236.0, 5236.2, -0.02, "lt"],
                          [5197.0, 5199.0, -0.045, "lt"]],

                    44 : [[5280.0, 5280.4, -0.017, "lt"],
                          [5276.4, 5277.0, -0.015, "lt"], 
                          [5271.0, 5271.4, -0.02, "lt"]],

                    45 : [[5355.5, 5356.0, -0.04, "lt"],
                          [5355.5, 5356.0, 0.02, "gt"],
                          [5340.4, 5340.44, -0.018, "lt"], 
                          [5340.4, 5340.44, 0.01, "gt"],
                          [5340.22, 5340.26, 0.008, "gt"],
                          [5340.22, 5340.26, -0.015, "lt"],
                          [5320.8, 5322.8, 0.01, "gt"],
                          [5320.8, 5322.8, -0.019, "lt"],
                          [5317.0, 5319.0, -0.019, "lt"]],

                    51 : [[5616.5, 5617.5, -0.02, "lt"]],

                    56 : [[5918.19, 1918.23, 0.1, "gt"],
                          [5891.0, 5892.0, -0.6, "lt"], 
                          [5891.4, 5891.6, -0.5, "lt"]],

                    67 : [[6564.5, 6564.92, -0.04, "lt"],
                           [6565.71, 6565.91, 0.015, "gt"]],
                          #[[6564.4, 6564.92, -0.04, "lt"]],

                          #[[6564.3, 6564.92, -0.04, "lt"],
                         # [6563.11, 6563.60, -0.027, "lt"], 
                         # [6568.96, 6569.45, -0.025, "lt"],
                         # [6563.65, 6564.16, -0.022, "lt"],
                          #[6563.80, 6564.39, 0.01, "gt"]],
                         # [6565.23, 6568.09, 0.015, "gt"]],
                          #[6562.02, 6562.15, 0.01, "gt"]],

                    80 : [[7666.1, 7666.4, -0.05, "lt"]],

                    81 : [[7700.2, 7700.3, -0.03, "lt"]],

                    84 : [[8103.0, 8104.0, -0.45, "lt"], 
                          [8081.51, 8081.59, -0.09, "lt"], 
                          [8081.37, 8082.61, 1.04, "gt"], 
                          [6991.0, 6991.2, 1.05, "gt"]]
                          
                           
                  }

  order_filtered_fnames = {}  

  # 1: Check if any spectra have a pixel in filter regions < threshold. If they
  #    do, add it to that orders filtered spectra
  for order, shard in shard_dict.items():
    order_filtered_fnames[order] = set()
    for fname, spectrum in shard.spectra.items():
      if order in filter_regions.keys():
        for lo_wv, hi_wv, threshold, threshold_type in filter_regions[order]:
          #print(lo_wv, hi_wv, threshold)
          lo_px = np.argmax(spectrum.lin_x > lo_wv) - 1
          hi_px = np.argmax(spectrum.lin_x > hi_wv)
          if threshold_type == "lt" and \
             np.any(spectrum.log_y[lo_px:hi_px] < threshold):
            order_filtered_fnames[order].add(fname)
          elif threshold_type == "gt" and \
             np.any(spectrum.log_y[lo_px:hi_px] > threshold):
            order_filtered_fnames[order].add(fname)

  # 2: Remove all filtered spectra 
  for order, filtered_fnames in order_filtered_fnames.items():
    if order in shard_dict:
      for filtered_fname in filtered_fnames:
        del shard_dict[order].spectra[filtered_fname]
        if order == 67:
          print(filtered_fname)


        
