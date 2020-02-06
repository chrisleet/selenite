from astropy.io import fits
from glob import glob
import matplotlib.pyplot as plt
import numpy as np

def plot_spectrum():

  np.seterr(all='raise')

  # 0: Program constants
  order = 80

  # 1(a): Get spectrum names
  all_spectrum_names = glob("/home/chrisleet/astronomy/data/fitspec/201*/*/HR*")
  #all_spectrum_names = glob("/home/chrisleet/HR*")
  #print(all_spectrum_names)

  # 1(b): Get bad spectrum
  bad_spectrum_f = open(("/home/chrisleet/astronomy/expres_pipeline/expres"
                        "/selenite/config/bad_spectra.txt"), "r")
  #bad_spectrum_f = open("bstars.txt")
  bad_spectrum = []
  for line in bad_spectrum_f:
    bad_spectrum.append(line[:-1])

  # 1(c) Remove bad spectrum from spectrum names
  spectrum_names = set(all_spectrum_names) - set(bad_spectrum)

  #spectrum_names = set(bad_spectrum)

  # 2: Open each spectrum.
  files = {}

  for fname in spectrum_names:

    files[fname] = {}
    f = fits.open(fname, do_not_scale_file=True)

    lin_x = f[1].data.wavelength[order]
    lin_y = f[1].data.spectrum[order]
 
    lin_x = lin_x[np.logical_not(np.isnan(lin_y))]
    lin_y = lin_y[np.logical_not(np.isnan(lin_y))]

    lin_y[lin_y < 0.01] = 0.01

    files[fname]["lin_x"] = lin_x 
    files[fname]["lin_y"] = lin_y

  # 3: Print out spectrum with 0 as their wavelength
  print("Files with no wavelength:")
  for fname, spectrum in files.items():
    if spectrum["lin_x"][0] < 100:
      #print("{}".format(fname.split("/")[-1]))
      print(fname)

  # 4: Print out spectrum with no lines in spectrum:
  print("Files with very low counts:")
  for fname, spectrum in files.items():
    try:
      np.log(spectrum["lin_y"]) < -3.0
    except:
      print(spectrum["lin_y"])

    if np.any(np.log(spectrum["lin_y"]) < -3.0):
      #print("{}".format(fname.split("/")[-1]))
      print(fname)


  # 5: Plot spectrum
  fig = plt.figure(facecolor="white")
  for fname, spectrum in files.items():
    plt.plot(spectrum["lin_x"], np.log(spectrum["lin_y"]))
  plt.show()

  


if __name__ == "__main__":
  plot_spectrum()
