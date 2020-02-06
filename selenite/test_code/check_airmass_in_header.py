import numpy as np

from astropy.io import fits
from glob import glob
from os import mkdir
from os.path import isdir, join
from shutil import copyfile

def check_airmass_in_header(date, source):

  # 1: Get spectra to check
  source_pattern = join(source, "*", date, "*" + ".fits")
  source_spectra = sorted(glob(source_pattern))

  # 2: Check spectra
  for fname in source_spectra:
    f = fits.open(fname, do_not_scale_file=True)
    if "AIRMASS" not in f[0].header:
      print(fname.split("/")[-1])
    f.close()

if __name__ == "__main__":
  for date in ["180703", "180704", "180705"]:
    check_airmass_in_header(date, "/expres/extracted/fitspec")
