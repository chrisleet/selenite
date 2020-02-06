import matplotlib.pyplot as plt
import numpy as np

from scipy.interpolate import interp1d

def generate_pwv_metric(shard_dict):

  # PWV metric is the intensity of the telluric spectrum @ 6940.18A (in 
  # order 72)

  # 1: Get section of telluric spectrum that contains 6940.18A
  target_order = 72
  target_wv = 6940.18
  wv_buffer = 3
  l_cutoff_wv, r_cutoff_wv = target_wv - wv_buffer, target_wv + wv_buffer
  spectrum =  next(iter(shard_dict[target_order].spectra.values()))
  l_cutoff_px = np.argmax(spectrum.lin_x > l_cutoff_wv)
  r_cutoff_px = np.argmax(spectrum.lin_x > r_cutoff_wv)
  lin_x = spectrum.lin_x[l_cutoff_px:r_cutoff_px]
  log_y = spectrum.log_y[l_cutoff_px:r_cutoff_px]

  # 2: Interpolate telluric spectrum section
  continuous_spectrum = interp1d(spectrum.lin_x, spectrum.log_y, kind=3, 
                                 bounds_error=False, fill_value=0.0)

  # 3: Generate pwv metric
  pwv = continuous_spectrum(target_wv)

  # 4: Compare continuous and exact spectrum
  plot_pwv_metric = False
  if plot_pwv_metric:
    fig = plt.figure(facecolor="white")
    plt.plot(lin_x, log_y)
    upsampled_lin_x = np.linspace(lin_x[0], lin_x[-1], len(lin_x)*10)
    plt.plot(upsampled_lin_x, continuous_spectrum(upsampled_lin_x))
    plt.scatter([target_wv], [pwv], color="r", marker="X")
    plt.show()

  # 5: Format PWV
  formatted_pwv = "{:.3f}".format(np.exp(pwv))

  return formatted_pwv
