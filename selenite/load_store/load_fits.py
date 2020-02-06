from astropy.io import fits
from glob import glob
from os.path import join
import numpy as np

from data_containers import shard

def load_star_at_path(path, config):

  # 1: Get orders and transition dates
  orders = get_orders(config)

  # 2: Create wv grid shard dict
  shard_dict = {}
  load_star(path, shard_dict, orders)
  return shard_dict


def load_bstars(bstar_path, bad_bstar_path, config):

  # 1: Find all B star files
  pattern = join(bstar_path, "201*", "*", "*HR*")
  fnames = glob(pattern)

  # 2: Remove bad B star files
  bad_bstar_fnames = [l[:-1] for l in open(bad_bstar_path, "r")]
  fnames = set(fnames) - set(bad_bstar_fnames)

  # 3: Get orders and transition dates
  orders = get_orders(config)
  
  # 4: Create shard dict
  shard_dict = {}
  for fname in fnames:
    load_star(fname, shard_dict, orders)
  return shard_dict


def get_orders(config):

  # 1: Get orders
  orders = config["orders"]
  if config["orders"] == "all":
    orders = np.arange(38,86)

  return orders


def load_star(fname, shard_dict, orders):

  # 1: Open star's file
  f = fits.open(fname, do_not_scale_image_data=True)


  # 2: Load selected orders into shard_dict
  for order in orders:

    # 2(a): Get shard lin_x, lin_y, airmass, continuum and uncertainities
    lin_x = f[1].data.wavelength[order]
    lin_y = f[1].data.spectrum[order]
    continuum = f[1].data.continuum[order]
    uncertainty = f[1].data.uncertainty[order]
    z = float(f[0].header["AIRMASS"])

    # 2(b): Strip nans
    good_px = np.logical_not(np.isnan(lin_y))
    print("good_px len", len(good_px))
    lin_x = lin_x[good_px]
    lin_y = lin_y[good_px]
    continuum = continuum[good_px]
    uncertainty = uncertainty[good_px]
    snrs = lin_y / uncertainty
    print("lin_y", lin_y)

    # 2(c): If a shard doesn't exist for the current order in shard_dict,
    #       create one.
    if order not in shard_dict:
      shard_dict[order] = shard.Shard(order)

    # 2(d): Set all lin_y data < 0.00001 to 0.00001, and then log lin_y.
    MIN_LIN_VAL = 0.00001 #0.01
    try:
      lin_y[lin_y < MIN_LIN_VAL] = MIN_LIN_VAL
    except:
      print(lin_y)
    log_y = np.log(lin_y)

    # 2(e): Store results
    shard_dict[order].spectra[fname] = shard.Spectrum_Data(lin_x, log_y, z, \
                                        continuum, uncertainty, snrs)


