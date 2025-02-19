import numpy as np

from os import listdir
from os.path import join

from data_containers import shard

def load_normalized_bstars(normed_bstar_path, orders):

  # 1: Get normalized B star names
  fnames = [f for f in listdir(normed_bstar_path) if f.endswith(".npz")]
  fnames = [join(normed_bstar_path, f) for f in fnames]

  # 2: Construct shard dict
  shard_dict = {}
  for fname in fnames:
    f = np.load(fname)
    for obj_name, obj in f.items():

      # 2(a): Get order/data type of current object
      order, obj_type = obj_name.split(".")
      order = int(order)

      if orders != "all" and order not in orders:
        continue

      # 2(b): Add shard with current order if one does not exist
      if order not in shard_dict:
        shard_dict[order] = shard.Shard(order)

      # 2(c): Save object to shard's spectrum
      if fname not in shard_dict[order].spectra:
        shard_dict[order].spectra[fname] = \
          shard.Spectrum_Data(None,None,None,None,None,None)

      if obj_type == "lin_x":
        shard_dict[order].spectra[fname].lin_x = obj
      elif obj_type == "log_y":
        shard_dict[order].spectra[fname].log_y = obj
        shard_dict[order].spectra[fname].px_no = len(obj)
      elif obj_type == "z":
        shard_dict[order].spectra[fname].z = obj
      elif obj_type == "l_cutoff_wv":
         shard_dict[order].l_cutoff_wv = obj
      elif obj_type == "r_cutoff_wv":
        shard_dict[order].r_cutoff_wv = obj
      else:
        raise Exception("obj_type {} not recognized.".format(obj_type))
        
  return shard_dict
