import os

from astropy.io import fits
import numpy as np

from . import db_indicies as dbi
from . import load_fits

# Indicies of fits file arrays2018/180625/101501_180625.1129.fits
FLG_IND = 4
TEL_DIV_IND = 5

def write_back_tellurics(spectrum_path, model, pwv, order_wv_ranges, shards):

  # 1: Open file
  f = fits.open(spectrum_path, do_not_scale_image_data=True)

  # 2: Write telluric divided spectrum
  for order in range(0, 86):
    if order in shards:
      #only one spectrum in shard
      spectrum = next(iter(shards[order].spectra.values())) 

      # 2(a) Create tellurics array filled with nans
      tellurics = np.zeros(len(f[1].data.tellurics[order]))
      tellurics.fill(np.nan)

      # 2(b) Find the pixel at which the calculated telluric spectrum starts/
      # ends, and paste it into array
      l_cutoff_wv, r_cutoff_wv = order_wv_ranges[order]
      l_cutoff_px = np.argmax(f[1].data.wavelength[order] > l_cutoff_wv)
      r_cutoff_px = np.argmax(f[1].data.wavelength[order] > r_cutoff_wv)
      good_px=np.where(np.logical_not(np.isnan(f[1].data.spectrum[order])))[0]
      l_cutoff_px = l_cutoff_px if l_cutoff_px > good_px[0] else good_px[0]
      r_cutoff_px = r_cutoff_px if r_cutoff_px < good_px[-1] else good_px[-1]
      tellurics[l_cutoff_px:r_cutoff_px] = spectrum.tel_lin_y

      # 2(c) Set telluric array in file
      f[1].data.tellurics[order] = tellurics
    else:
      f[1].data.tellurics[order] = np.ones(len(f[1].data.tellurics[order]))

    
      
  # 3: Write PWV to header
  pwv_msg = "Calculated telluric intensity at 6940.18A"
  f[1].header.set("PWV", pwv, pwv_msg)

  # 4: Overwrite
  f.writeto(spectrum_path, overwrite=True)
  f.close()


def write_PWV_header(spectra_folder, out_folder, calibrators):

  """
  Writes CRYSTAL's PWV metric to calibration spectra headers
  """
  
  w_calibrator, z_calibrator, f_order = calibrators
  
  for PWV, filename in zip(w_calibrator, f_order):
    spectrum_path = os.path.join(spectra_folder, filename)
    f = fits.open(spectrum_path, do_not_scale_image_data=True)
    f[0].header["SEL_PWV"] = abs(PWV) 
    f.writeto(os.path.join(out_folder, filename))
    f.close()
                  


#def write_tellurics_to_fits(spectrum_path, out_folder, model, mu, shards):

#  # 1: Open file
#  f = fits.open(spectrum_path, do_not_scale_image_data=True)

#  # 2: Write telluric flags
#  order_shift = 0
#  if load_fits.find_epoch_from_date(f[0].header["DATE-OBS"]) == 2:
#    order_shift = 1

#  for row in model:
#    f[0].data[int(row[dbi.ORD_IND]) + order_shift, int(row[dbi.PX_IND]), FLG_IND] = 2

#  # 3: Write telluric divided spectrum
#  for shard in shards.values():
#    spectrum = next(iter(shard.spectra.values())) #only one spectrum in shard
#    f[0].data[shard.order + order_shift, shard.lo_px:shard.hi_px, TEL_DIV_IND] = spectrum.tel_lin_y

#  # 4: Write PWV to header
#  #f[1].header["PWV"] = str(np.exp(mu))
#  f[0].header["CALC-PWV"] = str(np.exp(mu))
#  #print("write_fits: CALC-PWV:{}".format(f[0].header["CALC-PWV"]))
#  
#  # 5: Open destination and write
#  out_filename = os.path.basename(os.path.splitext(spectrum_path)[0]) + "t.fits"
#  out_path = os.path.join(out_folder, out_filename)
#  f.writeto(out_path, overwrite=True)
#  f.close()
