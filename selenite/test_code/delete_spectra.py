import numpy as np

from glob import glob
from os import mkdir, remove
from os.path import isdir, join
from shutil import copyfile

def delete_spectra(date):

  # 1: Get spectra to copy
  source_pattern = join("/home/chrisleet/astronomy/data/fitspec", "*", date, "*" + ".fits")
  source_spectra = sorted(glob(source_pattern))
  

  source_spectra = [s for s in source_spectra if "Flat" not in s and \
                    "LFC" not in s and "HR" not in s and "ThAr" not in s and \
                    "temp" not in s and "101501" not in s and "217014" not in s and \
                    "75732" not in s]
  print(source_spectra)

  for s in source_spectra:
    remove(s)

if __name__ == "__main__":
  for date in ["180622"]:
    delete_spectra(date)
