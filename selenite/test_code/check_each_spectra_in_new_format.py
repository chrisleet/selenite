from astropy.io import fits
from glob import glob
from os.path import join

def check_spectra_format(spectra, source):

  # 1: Get spectra to check
  source_pattern = join(source, "*", "*", spectra + "*" + ".fits")
  source_spectra = sorted(glob(source_pattern))
  
  # 2: Check spectra
  print("Not new format spectra:")
  for s in source_spectra:
    f = fits.open(s, do_not_scale_image=True)
  
    if len(f[1].data.spectrum) != 86 or len(f[1].data.spectrum[72]) != 7920:
      print(s) #s[39:])
      #print("orders:", len(f[1].data.spectrum), 
      #      "order_len:", len(f[1].data.spectrum[72])) 
    f.close()
  print("Done")

if __name__ == "__main__":
  check_spectra_format("HR", "/home/chrisleet/astronomy/data/fitspec")
