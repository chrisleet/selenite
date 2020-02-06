import os
import yaml

import get_args.get_calibrate_args as get_calibrate_args

import load_store.load_fits as load_fits
import load_store.load_normalized_spectra as load_norms
import load_store.write_db as write_db
import load_store.write_normalized_spectra as write_norms

import model.cluster_analysis as cluster_analysis
import model.regression_model as regression_model
import model.telluric_identification as telluric_id

import preprocessing.align_spectra as align_spectra
import preprocessing.constrain_wvs as constrain_wvs
import preprocessing.filter_bstars as filter_bstars
import preprocessing.suppress_stellar_lines as supression

import visualize.plot_data as plot_data
import visualize.plot_PCCs as plot_PCCs
import visualize.plot_regressions as plot_regressions
import visualize.plot_property as plot_property

def calibrate_selenite(wv_grid_path, db_path, config_path):

  # 1) LOAD DATA
  # Loads: (a) config, (b) calibration spec., (c) a wavelength grid spec.
  # Stores each calibration spec. order in a data container called a shard.
  # Produces dictionary linking each shard to its order.
  config = yaml.safe_load(open(config_path, "r"))
  shard_dict = load_norms.load_normalized_bstars(config["normed_bstar_path"], 
                                                 config["orders"])
  wv_grid_shard_dict = load_fits.load_star_at_path(wv_grid_path, config)
  plot_data.plot_data(shard_dict, "wv", "log", config["plot_norm_data"], 
                      "after normalization")
  print(list(shard_dict.keys()))

  # 2) FILTER BSTARS, SUPRESS LINES
  # Filter out all b stars with unflattened stellar lines/supress these lines
  filter_bstars.filter_bstars_with_unflatted_stellar_lines(shard_dict)
  supression.suppress_stellar_lines(shard_dict)
  plot_data.plot_data(shard_dict, "wv", "log", config["plot_filtered_data"], 
                      "after filtering")

  # 3) CONSTRAIN WV_GRID TO GOOD WV RANGE
  constrain_wvs.constrain_wv_grid_wvs(shard_dict, wv_grid_shard_dict)


  # 4) ALIGN BSTARS TO WAVELENGTH GRID
  align_spectra.align_spectra(shard_dict, wv_grid_shard_dict)
  plot_data.plot_data(shard_dict, "wv", "log", config["plot_aligned_data"], 
                          "after alignment")
  
  # 5) IDENTIFY TELLURIC PIXELS
  # i)   Get calibration line/calibration line suite data.
  # ii)  Identify pixels with significant PCC with either a) a H20 calibration line or b) z, 
  #      or that are saturated.
  # iv)  Remove all 1 and 2 telluric pixel clusters.
  # v)   Remove all telluric clusters not in the shape of a Gaussian trough.
  # vi)  Remove all telluric clusters more than 1nm from another cluster.
  # vii)  Mark each cluster as non-water, water, or both.
  calibrator_px = telluric_id.find_calibrator_px(shard_dict, config)
  calibrators = telluric_id.generate_calibrators(shard_dict, calibrator_px)
  plot_property.plot_property(shard_dict, calibrators, "z", "wavelength", 
                                            calibrator_px, config["plot_shard_zs"])
  plot_property.plot_property(shard_dict, calibrators, "PWV_out", "wavelength",
                                            calibrator_px, config["plot_shard_PWVs"])

  k = telluric_id.compute_PCC_threshold(config["p_value"], config["thresholds_file"])
  telluric_id.flag_high_PCC_pixels(calibrators, k, shard_dict, config)
  cluster_analysis.identify_clusters(shard_dict)
  plot_PCCs.plot_coadd_spec_PCCs(shard_dict, "water", False, config["plot_water_PCCs"])
  plot_PCCs.plot_coadd_spec_PCCs(shard_dict, "airmass", False,  config["plot_z_PCCs"])
  plot_PCCs.plot_coadd_spec_PCCs(shard_dict, "water", True,  config["plot_water_px"])
  plot_PCCs.plot_coadd_spec_PCCs(shard_dict, "airmass", True,  config["plot_z_px"])

  cluster_analysis.remove_1_and_2_pixel_clusters(shard_dict)
  plot_PCCs.plot_coadd_spec_PCCs(shard_dict, "airmass", True, config["plot_z_px_no_fp"], "1")
  cluster_analysis.remove_non_trough_clusters(shard_dict, config)
  plot_PCCs.plot_coadd_spec_PCCs(shard_dict, "airmass", True, config["plot_z_px_no_fp"], "2")
  cluster_analysis.remove_isolated_clusters(shard_dict)
  plot_PCCs.plot_coadd_spec_PCCs(shard_dict, "airmass", True, config["plot_z_px_no_fp"], "3")
  
  # 6) EXPAND CLUSTERS
  # Expand each cluster by one pixel on either side to pick up pixels in its line's tail.
  cluster_analysis.expand_clusters(shard_dict)
  fp_ttl = "w/ fp removal (& expansion)"
  plot_PCCs.plot_coadd_spec_PCCs(shard_dict, "water", True, config["plot_water_px_no_fp"], fp_ttl)
  plot_PCCs.plot_coadd_spec_PCCs(shard_dict, "airmass", True, config["plot_z_px_no_fp"], fp_ttl)

  # 7) RESOLVE OVERLAPPING CLUSTERS
  # Resolve overlapping water and non-water clusters.
  cluster_analysis.resolve_same_class_overlapping_clusters(shard_dict)
  cluster_analysis.resolve_diff_class_overlapping_clusters(shard_dict)
  plot_PCCs.plot_px_classification(shard_dict, config["plot_px_classification"])

  # 8) GENERATE REGRESSION MODEL
  # Generate a regression model for each telluric pixel.
  regression_model.find_regression_coeffs(shard_dict, calibrators, config)
  plot_regressions.plot_regressions(shard_dict, calibrators, config)
  
  # 9) WRITE MODEL TO DATABASE
  # Write out model to database.
  write_db.write_db(db_path, shard_dict, calibrators)

  # 10) ALERT THAT SPECTRUM IS COMPLETE
  #os.system('say "spectrum model complete"')
    
def run_calibrate_selenite_from_cmnd_line():

    args = get_calibrate_args.get_calibrate_args()
    calibrate_selenite(args.wv_grid_path, args.db_path, args.config_path)

if __name__ == "__main__":
    run_calibrate_selenite_from_cmnd_line()
