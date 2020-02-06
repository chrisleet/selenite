import numpy as np

global ST_IND
ST_IND = 0
global END_IND
END_IND = 1

def find_regression_coeffs(shards, calibrators, config):

  """
  Build a regression model for each telluric pixel & save regression coeffs.

  The regression model for water pixels is built by regression against the
  water calibrator, the regression model for non-water builds is built by
  regression against airmass.

  Notes
  -----
  The order in which spectrum appear in each calibrator is saved, and 
  spectra's depths' at the current telluric pixel are appended in that order
  to make sure that the regression's x and y values are in the right order.
  """

  w_calibrator, z_calibrator, f_order = calibrators

  for shard in shards.values():

    for clusters, coeffs, calibrator in zip([shard.w_clusters, shard.z_clusters],
                                            [shard.w_coeffs, shard.z_coeffs],
                                            [w_calibrator, z_calibrator]):
      for cluster in clusters:
        for px in range(cluster[ST_IND], cluster[END_IND]+1):

          # 1: Get calibrator values/px depths for pixel
          px_calibrator, px_depths = [], []
          for file_cal, filename in zip(calibrator, f_order):
            if filename in shard.spectra:
              px_calibrator.append(file_cal)
              px_depths.append(shard.spectra[filename].log_y[px])
          px_calibrator,px_depths = np.array(px_calibrator),np.array(px_depths)
          
          # 2: Make mask that selects datapoints with unsaturated depths
          unsat_px = px_depths >= config["saturation_threshold"]

          # 3: Regress on unsaturated datapoints
          m, c = np.polyfit(px_calibrator[unsat_px], px_depths[unsat_px], 1)
          coeffs[px] = (m, c)

            
