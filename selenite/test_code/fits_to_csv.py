import matplotlib.pyplot as plt

from astropy.io import fits

def fits_to_csv():

  fits_file_name = ("./examples/217014_190607.1101.csv")
  f = fits.open(fits_file_name + ".fits", do_not_scale_image=True)

  order = 72

  # Test: plot spectrum
  plot_spectrum = True
  if plot_spectrum:
      fig = plt.figure(facecolor="white")
      plt.plot(f[1].data.wavelength[order], f[1].data.spectrum[order]) 
      plt.show()
  
  # Write spectrum order to csv
  out = open(fits_file_name + ".csv", "w")
  out.write("wv,intens\n")
  for i in range(len(f[1].data.wavelength[order])):
    data_pt_str = "{},{}\n".format(f[1].data.wavelength[order][i], 
                                   f[1].data.spectrum[order][i])
    out.write(data_pt_str)
  
  f.close()
  out.close()

if __name__ == "__main__":
  fits_to_csv()
