import argparse

from utility import read_args_utility

def get_fit_args():

  """
  Reads command-line arguments for generate_telluric_model.
  """

  parser = argparse.ArgumentParser(
                      description="fits telluric model to a science spectrum")

  parser.add_argument("science_spectrum", metavar="science_spectrum", 
                      help="science spectrum to fit telluric model to")

  parser.add_argument("db_path", type=read_args_utility.is_csv_file, 
                      metavar="telluric_db_path {*.csv}", 
                      help="path to telluric model db")

  parser.add_argument("config_path", type=read_args_utility.is_yaml_file,
                      metavar="config {*.yml}", help="fitter config file")

  args = parser.parse_args()

  return args
    
    
