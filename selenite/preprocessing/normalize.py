import matplotlib.pyplot as plt
import numpy as np

def normalize(shard_dict): 
  """
  Normalizes each spectrum.

  Fits a polynomial to each spectrum's baseline, and then divides this 
  polynomial out. We make sure that the polynomial fit isn't affected by
  the lines in the spectrum by dividing the spectrum up into sets,
  fitting a line to each set, and then only fitting the polynomial to 
  the pixels above each line.
  """

  ORDERS_TO_CONTINUUM_NORMALIZE = [71,79,80,75,76]
  
  for order, shard in shard_dict.items():
    if order in ORDERS_TO_CONTINUUM_NORMALIZE:
      continuum_normalize(shard)
    else:
      polyfit_normalize(order, shard)

def continuum_normalize_all_orders(shard_dict):
  for order, shard in shard_dict.items():
    continuum_normalize(shard)


# Normalize shard's spectrum using the provided continuum
def continuum_normalize(shard):
  for spectrum in shard.spectra.values():
    spectrum.log_y = np.log(np.exp(spectrum.log_y) / spectrum.continuum)

# Normalize shard's spectrum by fitting a polynomial baseline to them
def polyfit_normalize(order, shard):

  plot_baseline_fitter = False

  for fname, spectrum in shard.spectra.items():
   
    SHARD_SLICES_NO = 11
    shard_slice_px = np.linspace(0,spectrum.px_no,SHARD_SLICES_NO+1,dtype=int)

    SLICE_BUF_LEN = 175
    normalized_slices = []

    for i in range(SHARD_SLICES_NO):
      px_lo, px_hi = shard_slice_px[i], shard_slice_px[i+1]
      buf_lo, buf_hi = 0, 0

      if px_lo > SLICE_BUF_LEN:
        buf_lo = SLICE_BUF_LEN

      if px_hi < spectrum.px_no - SLICE_BUF_LEN:
        buf_hi = SLICE_BUF_LEN
      
      lin_x = spectrum.lin_x[px_lo-buf_lo : px_hi+buf_hi]
      log_y = spectrum.log_y[px_lo-buf_lo : px_hi+buf_hi]

      set_len, poly_fit = 300, 10
      if order < 51:
        set_len, poly_fit = 200, 20
      elif order == 67:
        set_len, poly_fit = 200, 30

      log_y = remove_baseline(np.copy(lin_x), np.copy(log_y), shard.order, 
                              px_lo-buf_lo, px_hi+buf_hi, buf_lo, buf_hi,
                              set_len, poly_fit, plot_baseline_fitter)
      
      if buf_hi == 0:
        normalized_slices.append(log_y[buf_lo:])
      else:
        normalized_slices.append(log_y[buf_lo:-buf_hi])

    for i in range(SHARD_SLICES_NO):
      px_lo, px_hi = shard_slice_px[i], shard_slice_px[i+1]
      spectrum.log_y[px_lo:px_hi] = normalized_slices[i]

    if plot_baseline_fitter:
      fig = plt.figure(facecolor="white")
      plt.plot(spectrum.lin_x, spectrum.log_y)
      plt.show()


    

def remove_baseline(lin_x, log_y, order, px_lo, px_hi, buf_lo, buf_hi,
                    set_len, poly_deg, plot_baseline_fitter):

  """
  Normalizes the data set lin_x, log_y
  """

  set_x, set_f, rdat_x, rdat_y = [], [], [], []
  set_no = int(len(log_y)/set_len)

  for set_i in range(set_no+1):

    #Select set of data points
    x = np.array(lin_x[set_i*set_len:(set_i+1)*set_len])
    y = np.array(log_y[set_i*set_len:(set_i+1)*set_len])

    if len(x) < 5:
      break   

    #Fit and store linear fit to data points
    f = np.poly1d(np.polyfit(x, y, 1))
    set_x.append(x)
    set_f.append(f)
    
    #Filter out data points below linear fit
    set_filtered_pts_x, set_filtered_pts_y = [], []
    for i in range(len(x)):
      if(y[i] >= f(x[i])):
        set_filtered_pts_x.append(x[i])
        set_filtered_pts_y.append(y[i])
    
    # Filter out all data points more that MAX_RANGE below 95th percentile pt
    # unless @ stellar feature (e.g. Na-D, H-alpha, )
    if (order == 56 and px_hi < 3000) or \
       (order == 67 and px_hi < 4000) or \
       (order == 81 and px_lo > 3000):
      max_range = 1.0
    else:
      max_range = 0.03

    try:
      peak_y = np.percentile(set_filtered_pts_y, 97)
      #plot_baseline_fitter = False
    except:
      print(set_filtered_pts_y)
      #plot_baseline_fitter = True
  
    for i in range(len(set_filtered_pts_y)):
      if set_filtered_pts_y[i] > peak_y - max_range:
        rdat_x.append(set_filtered_pts_x[i])
        rdat_y.append(set_filtered_pts_y[i])

  # Convert data to reduce into a numpy array
  rdat_x = np.array(rdat_x)
  rdat_y = np.array(rdat_y)
  

  # Add extra points to the begining of a slice at the beginning of a order/
  # the end of a slice at the end of a order to stop fitting to the 
  # edges of an order producing odd results.
  if buf_lo == 0 or buf_hi == 0:
    EX_PTS = 20
    x_fit = np.poly1d(np.polyfit(np.arange(len(lin_x)), lin_x, 2))

    if buf_lo == 0:
      rdat_x = np.concatenate((x_fit(np.arange(-EX_PTS, 0)), rdat_x))
      rdat_y = np.concatenate((np.ones(EX_PTS) * np.percentile(rdat_y[:30],75), 
                               rdat_y))
    else:
      rdat_x = np.concatenate((rdat_x,
                               x_fit(np.arange(len(lin_x),len(lin_x)+EX_PTS))))
      rdat_y = np.concatenate((rdat_y,
                               np.ones(EX_PTS)*np.percentile(rdat_y[-30:],75)))


  # Median subtract rdat_x
  median_x = np.median(rdat_x)
  rdat_x -= median_x

  polyfit = np.poly1d(np.polyfit(rdat_x, rdat_y, poly_deg)) 
  baseline_y = polyfit(lin_x - median_x)

  # This plots the baseline fit. Useful for debugging
  if plot_baseline_fitter or \
    (False and np.any((log_y - baseline_y) > 0.15) and px_hi > 3000):
    plot_baseline_fit(lin_x, log_y, set_x, set_f, median_x, baseline_y,
                      rdat_x, rdat_y, polyfit, order, px_lo, px_hi)
  log_y -= baseline_y
  return log_y

def plot_baseline_fit(lin_x, log_y, set_x, set_f, median_x, baseline_y,
                      rdat_x, rdat_y, polyfit, order, px_lo, px_hi):

  """
  Plots the baseline fitter's fitting process.
  """
  
  fig = plt.figure(facecolor='white')
  plt.title(("Logged data for order {}, px:({},{}) w/ baselines fitted"
             " ").format(order, px_lo, px_hi))
  plt.xlabel("Wavelength (Angstroms)")
  plt.ylabel("Log(Signal strength)")

  for set_i in range(len(set_x)):
    plt.plot(set_x[set_i], set_f[set_i](set_x[set_i]), color="red")
      
  plt.plot(lin_x, log_y, color="blue")
  plt.plot(rdat_x + median_x, rdat_y, color="green")
  plt.plot(rdat_x + median_x, polyfit(rdat_x), color="orange")
      
  plt.show()       

  fig = plt.figure(facecolor="white")
  plt.title(("Logged data for order {}, px:({},{}) w/ baseline removed:"
             " ".format(order, px_lo, px_hi)))
  plt.plot(lin_x, log_y - baseline_y)
  plt.show()     
