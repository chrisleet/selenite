import argparse
import numpy as np
import yaml
from time import strftime

import get_args.get_calibrate_args as get_calibrate_args

import load_store.load_fits as load_fits
import load_store.write_normalized_spectra as write_norms

import preprocessing.filter_bstars as filter_bstars
import preprocessing.normalize as normalize
import preprocessing.suppress_stellar_lines as supression
import preprocessing.remove_fringes as remove_fringes

import visualize.plot_data as plot_data
import visualize.plot_uncertainty as plot_uncertainty

from utility import read_args_utility

from expres.config import FITS_DIR, BAD_BSTAR_FILE, NORMED_BSTAR_DIR

def normalize_bstars():

  # 0) READ COMMAND LINE ARGUMENTS
  parser = argparse.ArgumentParser(description = "normalizes bstars")
  parser.add_argument("config", type=read_args_utility.is_yaml_file,
                      metavar="config {*.yml}", help="norm. config file")
  args = parser.parse_args()

  # 1) LOAD DATA
  # Loads: (a) config, (b) calibration spec., (c) a wavelength grid spec.
  # Stores each calibration spec. order in a data container called a shard.
  # Produces dictionary linking each shard to its order.
  np.seterr(all='raise')
  config = yaml.safe_load(open(args.config, "r"))
  shard_dict = load_fits.load_bstars(FITS_DIR, BAD_BSTAR_FILE, config)
  plot_data.plot_data(shard_dict, "wv", "log", config["plot_raw_data"])

  # 2) PREPROCESS B STARS
  # (i) Remove low SNR B stars, 
  # (ii) Truncate B stars down to high SNR wavelength ranges.
  plot_uncertainty.plot_bstar_snrs(shard_dict,config,config["plot_bstar_snrs"])
  filter_bstars.filter_lo_snr_bstars(shard_dict, config)
  plot_uncertainty.plot_bstar_snrs(shard_dict, config,
                                   config["plot_bstar_snrs_after_filtering"])

  remove_fringes.find_uncertainty_cutoffs(shard_dict, config)
  plot_uncertainty.plot_uncertainty_cutoffs(shard_dict,
                                            config["plot_bstar_uncertainty"])

  plot_uncertainty.plot_bstar_cutoffs(shard_dict, config["plot_bstar_cutoffs"])
  remove_fringes.remove_fringes(shard_dict)
  plot_uncertainty.plot_bstar_cutoffs(shard_dict, 
                                      config["plot_cut_bstar_cutoffs"])

  # 3) NORMALIZE B STARS
  normalize.normalize(shard_dict)
  plot_data.plot_data(shard_dict, "wv", "log", config["plot_norm_data"])
  
  # 4) SAVE RESULTS
  write_norms.write_normalized_spectra(shard_dict, NORMED_BSTAR_DIR)
  return
    
if __name__ == "__main__":
  normalize_bstars()
