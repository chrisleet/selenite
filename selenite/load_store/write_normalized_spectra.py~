from os.path import join
import numpy as np

def write_normalized_spectra(shard_dict, normed_bstar_path):
  
  norm_fs = {}
  
  for order, shard in shard_dict.items():
     for fname, spectrum in shard.spectra.items():
        if fname not in norm_fs:
          norm_fs[fname] = {}
        norm_fs[fname]["{}.lin_x".format(order)] = spectrum.lin_x
        norm_fs[fname]["{}.log_y".format(order)] = spectrum.log_y
        norm_fs[fname]["{}.z".format(order)] = spectrum.z
        norm_fs[fname]["{}.l_cutoff_wv".format(order)] = shard.l_cutoff_wv
        norm_fs[fname]["{}.r_cutoff_wv".format(order)] = shard.r_cutoff_wv

  for fname, data in norm_fs.items():
    fpath = join(normed_bstar_path, fname.split("/")[-1][:-5])
    np.savez(fpath, **data)
