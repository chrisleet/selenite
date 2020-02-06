import numpy as np

from glob import glob
from os import mkdir
from os.path import isdir, join
from shutil import copyfile

def copy_spectra_star(spectra, source, target):
  copy_spectra(join(source, "*", "*", spectra + "*" + ".fits"), source, target)

def copy_spectra_date(date, source, target):
  copy_spectra(join(source, "*", date, "*" + ".fits"), source, target)

def copy_spectra(source_pattern, source, target):

  # 1: Get spectra to copy
  print(source_pattern)
  source_spectra = sorted(glob(source_pattern))
  

  source_spectra = [s for s in source_spectra if "Flat" not in s and \
                    "LFC" not in s and "HR" not in s and "ThAr" not in s and \
                    "temp" not in s and "101501" not in s and "217014" not in s and \
                    "75732" not in s]
  print(source_spectra)
 
  # 2: Get spectra destinations
  destination_spectra = []
  for s in source_spectra:
    destination_spectra.append(target + s[len(source):])
    
  # 3: Copy spectra
  for i, s, d in zip(np.arange(len(source_spectra)), source_spectra, destination_spectra):

    print("Copying:", i, "/", len(source_spectra), s, d)

    year_destination_folder = join(target, s.split("/")[4])
    if not isdir(year_destination_folder):
      mkdir(year_destination_folder)

    month_destination_folder = join(target, s.split("/")[4], s.split("/")[5])
    if not isdir(month_destination_folder):
      mkdir(month_destination_folder)

    copyfile(s, d)

if __name__ == "__main__":
  for date in ["190503", "190505", "190513", "190515", "190518", "190701", "190815", "190816"]:
    copy_spectra_date(date, "/expres/extracted/fitspec", "/home/chrisleet/astronomy/data/fitspec")
    #copy_spectra_date(date, "/home/chrisleet/astronomy/data/fitspec", "/expres/extracted/fitspec")
  
  #copy_spectra("75732", "/home/chrisleet/astronomy/data/fitspec", "/expres/extracted/fitspec")


# Cleared
# ["180426", "180427", "180429", "180501", "180503", "180504", "180505"]
# ["180523", "180525", "180526", "180527", "180528"]
# ["180529", "180530", "180531"]
# ["180602", "180603", "180604"]
# ["180605", "180606", "180607", "180608", "180609", "180610", "180611"]
# ["180613", "180622", "180623", "180624", "180625", "180626"]
# ["180627", "180628", "180629"]
# ["180630", "180701"]
# ["180703", "180704", "180705", "180706", "180707", "180708", "180709"]
# ["180710", "180711", "180731", "180906", "181004", "181005"]
# ["181114", "181114b", "181115", "181116"]
# ["181118", "181206", "181208", "181209", "181211", "181120"]
# ["181213", "181214", "181215", "181216", "181218", "181220", "181231"]
# ["190131", "190131b", "190207"]
# ["190210", "190211", "190212", "190214", "190214b", "190225", "190228", "190302"]
# ["190303", "190305", "190306", "190308", "190309"]
# ["190311", "190312", "190314", "190315", "190316", "190317"]
# ["190327", "190419", "190423", "190425", "190426", "190427"]
# ["190503", "190504", "190505", "190506", "190511", "190513", "190515", "190518"]
# ["190522", "190524", "190525", "190526", "190530", "190531"] 
# ["190605", "190607", "190608", "190609", "190610", "190612"]
# ["190614", "190615", "190616", "190618", "190619", "190620", "190621"] 
# ["190623", "190624", "190626", "190630"]
# ["190701", "190704", "190724", "190724b", "190806", "190808", "190809"]
# ["190815", "190816", "190817", "190819", "190820", "190821"]
# ["190824", "190825", "190828", "190831", "190905", "190909", "190923"]

# Sent back
# 
# Tested
# ["180624", 
# Processed
# ["180625", "181114", "190608", "190617"]
# Copied
# [
# Pending

# Align
# ["190503", "190505", "190513", "190515", "190518", "190701", "190815", "190816"]

# ["190503", "190505", "190513", "190515", "190518", "190701", "190815", "190816"]


# Fix
# ["180601"]



