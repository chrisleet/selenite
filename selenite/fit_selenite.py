import os
import yaml

import load_store.load_fits as load_fits
import load_store.read_db as read_db
import load_store.write_fits as write_fits

import model.fit_model as fit_model
import model.get_calibrators as get_calibrators
import model.generate_model as generate_model
import model.generate_pwv_metric as generate_pwv_metric
import model.telluric_identification as telluric_id


import preprocessing.constrain_wvs as constrain_wvs
import preprocessing.normalize as normalize


import get_args.get_fit_args as get_fit_args

import visualize.plot_data as plot_data
import visualize.plot_model as plot_model



def fit_selenite(science_spectrum, db_path, config_path):
  
  # 1) LOAD DATA
  # Load external data for calibration. External data is: i) configuration
  # file, ii) filename of spectrum to reduce, iii) content of calibration
  # spectra. Loads calibration spectra contents into a data container for 
  # each order. These data containers are called shard_dict. Produces a 
  # dictionary linking each processed order to its shard.
  config = yaml.safe_load(open(config_path, "r"))
  db, order_wv_ranges = read_db.read_db(db_path)
  shard_dict = load_fits.load_star_at_path(science_spectrum, config)
  plot_data.plot_data(shard_dict, "wv", "log", config["plot_raw_data"])

  # 2) CONSTRAIN SPECTRA WAVELENGTHS
  constrain_wvs.constrain_science_spectrum_wvs(shard_dict, order_wv_ranges)
  

  # 3) NORMALIZE DATA
  normalize.continuum_normalize_all_orders(shard_dict)
  plot_data.plot_data(shard_dict, "wv", "lin", config["plot_norm_data"])

  # 4) FIND CALIBRATOR PX
  cal_pxs = telluric_id.find_calibrator_px(shard_dict, config)


  # 5) GENERATE TELLURIC SPECTRUM
  # i) Find mu by fitting the water calibrators' intensity to the sci. spectrum
  # ii) Retrieve z from science spectrum.
  # iii) Generate telluric spectrum for choice of mu and z
  # iv) Generate PWV metric
  mu = fit_model.get_mu(cal_pxs, shard_dict, db, config)
  z = fit_model.get_z(shard_dict)
  model = generate_model.generate_model(mu,z,db,config["saturation_threshold"])
  generate_model.generate_telluric_spectrum(shard_dict, model)
  pwv = generate_pwv_metric.generate_pwv_metric(shard_dict)
  plot_model.plot_model(shard_dict, model, pwv, "wavelength", 
                        show=config["plot_fit_telluric_spec"])

  # 6) WRITE OUT MODEL
  write_fits.write_back_tellurics(science_spectrum, model, pwv, order_wv_ranges, 
                                  shard_dict)

  # 7) ALERT THAT SPECTRUM IS COMPLETE
  #os.system('say "spectrum reduction complete"')

def run_fit_selenite_from_cmnd_line():

  args = get_fit_args.get_fit_args()
  fit_selenite(args.science_spectrum, args.db_path, args.config_path)

if __name__ == "__main__":
  run_fit_selenite_from_cmnd_line() 
