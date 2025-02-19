import numpy as np

from load_store import db_indicies as dbi

###########
# Globals #
###########

#Indices of fields in spectrum model
ORD_IND = 0
PX_IND = 1
WV_IND = 2
CLS_IND = 3
INT_IND = 4

def generate_model(mu, z, db, sat_threshold):

  """
  Combine mu and z values with telluric db to generate telluric model
  """

  model = []

  for record in db:
    if record[dbi.CLS_IND] == "w":
      f_w  = np.poly1d([record[dbi.RM_IND], record[dbi.RC_IND]])
      lin_intensity = np.exp(f_w(mu)) if f_w(mu) > sat_threshold else -1
    elif record[dbi.CLS_IND] == "z":
      f_z  = np.poly1d([record[dbi.RM_IND], record[dbi.RC_IND]])
      lin_intensity = np.exp(f_z(z)) if f_z(z) > sat_threshold else -1
    elif record[dbi.CLS_IND] == "c" or record[dbi.CLS_IND] == "s":
      lin_intensity = -1
    else:
      raise Exception("Record class '{}' unknown".format(record[dbi.CLS_IND]))
    model.append(record[dbi.ORD_IND:dbi.CLS_IND+1] + [lin_intensity])

  return model
            
def generate_telluric_spectrum(shards, model):

  """
  Generaes the telluric spectrum for each shard.
  """

  for shard in shards.values():

    spectrum = next(iter(shard.spectra.values())) #only one spectrum in shard
    spectrum.tel_lin_y = np.ones(len(spectrum.log_y))
    for row in model:
      px = row[PX_IND]
      if row[ORD_IND] == shard.order and px < len(spectrum.log_y):
        spectrum.tel_lin_y[px] = row[INT_IND]
  
    spectrum.div_lin_y = np.exp(spectrum.log_y) / spectrum.tel_lin_y
    spectrum.div_lin_y[spectrum.div_lin_y < 0] = 1
