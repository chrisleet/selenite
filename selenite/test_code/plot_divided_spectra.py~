import argparse
from astropy.io import fits
from glob import glob
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter

def plot_divided_spectra():

  # 0: Parse program arguments
  parser = argparse.ArgumentParser(description="plots divided raw spectra")
  parser.add_argument("-o", "--order", help="specify order to plot")
  parser.add_argument("-d", "--div_type", help="division to carry out")
  args = parser.parse_args()


  # 1(a): Get spectra names
  #all_spectra_names = glob("/home/chrisleet/astronomy/data/fitspec/201*/*/HR*")
  all_spectra_names = glob("/home/chrisleet/astronomy/data/fitspec/2018/180505/HR*")
  #print(all_spectra_names)

  # 1(b): Get bad spectra
  bad_spectra_f = open(("/home/chrisleet/astronomy/expres_pipeline/expres"
                        "/selenite/config/bad_spectra.txt"), "r")
  bad_spectra = []
  for line in bad_spectra_f:
    bad_spectra.append(line[:-1])

  # 1(c) Remove bad spectra from spectra names
  spectra_names = set(all_spectra_names) - set(bad_spectra)

  # 2: Open each spectra.
  files = {}
  for fname in spectra_names:
    files[fname] = fits.open(fname, do_not_scale_file=True)

  # 3: Get order(s) to plot
  if args.order is not None:
    orders = [int(args.order)]
  else:
    orders = list(range(37,82))

  # 4:Plot undivided spectra
  for order in orders: 

    # 4:Plot undivided spectra
    fig = plt.figure(facecolor="white")
    for fname, f in files.items():
      lin_x = f[1].data.wavelength[order]
      log_y = np.log(f[1].data.spectrum[order])
      plt.plot(log_y)

      if log_y[3000] > -1.6:
        print(fname) 

    plt.title("Order {}".format(order))
    plt.show()


    # 5: Plot divided spectra
    fig = plt.figure(facecolor="white")
    for fname, f in files.items():
      lin_x = f[1].data.wavelength[order]
      lin_y = regular_continuum_divide(f, order)
      log_y = np.log(lin_y)
      plt.plot(log_y)

     

    plt.title("Order {}".format(order))
    plt.show()

    



def regular_continuum_divide(f, order):
  return f[1].data.spectrum[order] / f[1].data.continuum[order]

def alpha_hull_continuum_divide(f, order):

  wv = f[1].data.wavelength[order].astype(np.float64)
  intens = f[1].data.spectrum[order].astype(np.float64)
  log_intens = np.log(intens)

  df = pd.DataFrame(data={"wv":wv, "intens":log_intens})
  df.astype('float64').dtypes
  print(df.dtypes)

  r_source = ro.r['source']
  r_source("afs_functions/AFS.R")
  r_AFS = ro.r['AFS']

  with localconverter(ro.default_converter + pandas2ri.converter):
    r_dataframe = ro.conversion.py2rpy(df)
    log_intes = r_AFS(r_dataframe, .95, .25)
    return np.exp(log_intens - 1), log_intes - 1
  

if __name__ == "__main__":
  plot_divided_spectra()

