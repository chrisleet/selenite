import sys

import matplotlib.pyplot as plt
import numpy as np

def plot_regressions(shard_dict, calibrators, config):

  """
  Plots each px selected in config's regression against its calibrator.

  Takes each pixel px in listed in config. Scatter plots the depth of 
  px for each spectrum against either (a) the average depth of the water 
  calibration lines if px is a water pixel or (b) airmass if px is a 
  non-water pixel, and then plots px's regression line over the scatter plot
  If px is neither a water pixel nor a non-water pixel, prints a message and
  does not produce a plot.
  """
  
  if not config["plot_regressions"]:
    return

  regression_targets = [(75, 3243), (75, 1822), (75, 5530), (75, 6483), (75, 6463), (75, 6134)]

  for order, px in regression_targets:
    if order in shard_dict:
      plot_px_regression(shard_dict[order], px, calibrators, 
                         config["saturation_threshold"])
    else:
      sys.stderr.write("Order %d not found, can't draw regression" % (order))

def plot_px_regression(shard, px, calibrators, saturation_threshold):

  """
  Plot the px in shard shard_addr's regression model with its calibrator.

  Worker function of plot regressions.
  """

  w_calibrator, z_calibrator, f_order = calibrators
  
  # 1: Get px depths at px
  print("Plotting regression at {}A".format(shard.spectra[f_order[0]].lin_x[px]))
  px_depths = []
  for filename in f_order:
    if filename in shard.spectra:
      px_depths.append(shard.spectra[filename].log_y[px])
  px_depths = np.array(px_depths)

  # 2: Make mask that selects datapoints with unsaturated depths
  unsat_px = px_depths >= saturation_threshold
  sat_px = px_depths < saturation_threshold
  
  # 3: Select the appropriate calibrator to plot regression model against, 
  #    and build regression model
  if px in shard.w_coeffs:
    r_model = np.poly1d(shard.w_coeffs[px])
    calibrator = w_calibrator
    cal_lbl = "Water calibrator"
  elif px in shard.z_coeffs:
    r_model = np.poly1d(shard.z_coeffs[px])
    calibrator = z_calibrator
    cal_lbl = "Airmass"
  else:
    sys.stderr.write("No regression for order %d px %d\n"%(shard.order,px))
    return

  # 4: Get r
  px_r = np.corrcoef(calibrator[unsat_px], px_depths[unsat_px])[0][1]

  # 5: Plot
  fig = plt.figure(facecolor='white')
  plt.xlabel(cal_lbl)
  plt.ylabel("Px {} log signal strength".format(px, shard.order))
  plt.title(("Order {}, px {}, regression w/ {} (r={:.2f})"
             " ").format(shard.order, px, cal_lbl, px_r))
  plt.scatter(calibrator[unsat_px], px_depths[unsat_px], marker="X", color="k")
  plt.scatter(calibrator[sat_px], px_depths[sat_px],  marker="X", color="r")

  cal_stuff = np.zeros(len(calibrator[unsat_px]) + 1)
  cal_stuff[:-1] = calibrator[unsat_px]
  plt.plot(sorted(cal_stuff), r_model(sorted(cal_stuff)),  "r--", zorder=2)
  plt.show()
      
