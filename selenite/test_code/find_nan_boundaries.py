from astropy.io import fits
from glob import glob
from os.path import join
import matplotlib.pyplot as plt
import numpy as np

def check_spectra_format(spectra, source):

  # 1: Get spectra to check
  source_pattern = join(source, "*", "*", spectra + "*" + ".fits")
  source_spectra = sorted(glob(source_pattern))

  # 2: Check spectra
#  order = 38
#  fig = plt.figure(facecolor="white")

#  for s_i, s in zip(range(len(source_spectra)), source_spectra):

#    f = fits.open(s, do_not_scale_image=True)
#    lin_y = f[1].data.spectrum[order]

#    fig_x, fig_y = [],[]
#    for y_i, y in zip(range(len(lin_y)), lin_y):
#      if np.isnan(y):
#        fig_x.append(y_i)
#        fig_y.append(s_i)

#    plt.scatter(fig_x, fig_y)

#    f.close()

#  plt.show()

  # 3: Generate all order overview
  lo_order, hi_order = 0, 86
  order_range = np.arange(lo_order, hi_order)
  lo_px = np.zeros(len(order_range))
  hi_px = np.ones(len(order_range)) * 7840

  for s in source_spectra:
    f = fits.open(s, do_not_scale_image=True)

    if len(f[1].data.spectrum) == 82:
      continue

    for order in order_range:
      lin_y = f[1].data.spectrum[order]

      order_lo_nans = np.where(np.isnan(lin_y[:1500]))[0]
      if len(order_lo_nans) > 0:
        order_lo_px = order_lo_nans[-1]
        if order_lo_px > lo_px[order - lo_order]:
          lo_px[order - lo_order] = order_lo_px

      order_hi_nans = np.where(np.isnan(lin_y[6000:]))[0]
      if len(order_hi_nans) > 0:
        order_hi_px = order_hi_nans[0] + 6000
        if order_hi_px < hi_px[order - lo_order]:
          hi_px[order - lo_order] = order_hi_px

  fig = plt.figure(facecolor="white")
  plt.plot(lo_px, order_range, "x-", color="black", label="lo_edge")
  plt.plot(hi_px, order_range, "x-", color="black", label="hi_edge")
  plt.xlabel("px")
  plt.ylabel("orders")
  
  plt.axvline(750, color="pink")
  plt.axvline(700, color="red")
  plt.axvline(600, color="pink")
  plt.axvline(500, color="red")
  plt.axvline(400, color="pink")
  plt.axvline(300, color="red")
  plt.axvline(250, color="orange")
  plt.axvline(200, color="yellow")
  plt.axvline(7000, color="red")
  plt.axvline(7100, color="orange")
  plt.axvline(7200, color="yellow")
  plt.axvline(7250, color="maroon")
  plt.axvline(7300, color="maroon")
  plt.axhline(38, color="blue")
  plt.axhline(8, color="green")
  plt.legend()
  plt.show()
      
    
    
  

if __name__ == "__main__":
  check_spectra_format("75732", "/home/chrisleet/astronomy/data/fitspec")
