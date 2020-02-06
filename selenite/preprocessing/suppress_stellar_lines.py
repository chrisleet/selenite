import numpy as np

# Supresses stellar lines in B stars
def suppress_stellar_lines(shard_dict):
  
  # 1: Order 56
  order = 56
  if order in shard_dict:
    for fname, spectrum in shard_dict[order].spectra.items():

      target = np.logical_and(spectrum.lin_x>5896.80, spectrum.lin_x<5897.96)
      spectrum.log_y[target] = 0.0

      target = np.logical_and(spectrum.lin_x>5890.77, spectrum.lin_x<5891.22)
      spectrum.log_y[target] = 0.0

      target = np.logical_and(spectrum.lin_x>5878.2, spectrum.lin_x<5878.95)
      spectrum.log_y[target] = 0.0

      target = np.logical_and(spectrum.lin_x>5891.17, spectrum.lin_x<5891.22)
      if np.any(spectrum.log_y[target] > -0.25):
         spectrum.log_y[target] = 0.0

  # 2: Order 84
  order = 84
  if order in shard_dict:
    for fname, spectrum in shard_dict[order].spectra.items():

      target = np.logical_and(spectrum.lin_x>8082.1, spectrum.lin_x<8082.5)
      spectrum.log_y[target] = 0.0

  # 3: Order 67
  order = 67
  if order in shard_dict:
    for fname, spectrum in shard_dict[order].spectra.items():

      target = np.logical_and(spectrum.lin_x>6563.06, spectrum.lin_x<6564.22)
      spectrum.log_y[target] = 0.0

      target = np.logical_and(spectrum.lin_x>6567.46, spectrum.lin_x<6568.22)
      spectrum.log_y[target] = 0.0

      target = np.logical_and(spectrum.lin_x>6560.60, spectrum.lin_x<6562.21)
      spectrum.log_y[target] = 0.0

      target = np.logical_and(spectrum.lin_x>6575.70, spectrum.lin_x<6576.52)
      spectrum.log_y[target] = 0.0

      target = np.logical_and(spectrum.lin_x>6541.95, spectrum.lin_x<6542.14)
      spectrum.log_y[target] = 0.0

      target = np.logical_and(spectrum.lin_x>6562.50, spectrum.lin_x<6562.75)
      spectrum.log_y[target] = 0.0

