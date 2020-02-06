import argparse

from utility import read_args_utility

def get_calibrate_args():

  """
  Reads command-line arguments for generate_telluric_model.
  """

  parser = argparse.ArgumentParser(description = \
    "generates a telluric model with cal spectra")

  parser.add_argument("wv_grid_path",
                      help="spectrum to take wavelength grid from")

  parser.add_argument("db_path", type=read_args_utility.is_csv_file, 
                      metavar="telluric_db_path {*.csv}", 
                      help="path to output telluric model db at")

  parser.add_argument("config_path", type=read_args_utility.is_yaml_file,
                      metavar="config {*.yml}", help="calibration config file")
  
  
  return parser.parse_args()
    
    
