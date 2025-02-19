import numpy as np

###########
# Globals #
###########

# NULL PCC value
NULL_INT = -10

# Indicies of shard address tuple
ORD_IND = 0
LOPX_IND = 1
HIPX_IND = 2

class Shard():

  """
  A shard is the primary data container for the telluric calibration code.

  A shard holds all data for a given range of wavelengths (e.g. spectra,
  PCCs of pixels, linear regression coefficients, etc.)

  Parameters
  ----------
  order: int
      The Echelle order the shard's data comes from.

  lo_px: int
      The low pixel number in the shard's range of pixels.

  hi_px: int
      The high pixel number in the shard's range of pixels.

  Attributes
  ---------
  order: int
      (see parameters)

  lo_pixel: int
      (see parameters)

  hi_pixel: int
      (see parameters)

  spectra: dict
      A dictionary mapping each calibration filename to a Spectrum_Data 
      object which contains its data.

  l_cutoff_wv, r_cutoff_wv : float
      The range of valid wavelengths in the order.

  w_PCCs: list (floats)
      The PCC of each pixel in the shard with the water calibrator.

  w_tel: list (booleans)
      Flags denoting whether each pixel has a water telluric component.

  w_clusters: list (tuples)
      Tuples giving the range of each cluster of water pixels in a spectrum.
      Note that w, z, sat, and composite clusters are non-overlapping after 
      processing.

  z_PCCs: list (floats)
      The PCC of each pixel in the shard with airmass.

  z_tel: list (booleans)
      Flags denoting whether each pixel has an air telluric component.

  z_clusters: list (tuples)
      Tuples giving the range of each cluster of z pixels in a spectrum.
      Note that w, z, sat, and composite clusters are non-overlapping after
      processing.

  sat_tel : list (booleans)
      Flags denoting whether each pixel is saturated or not.

  sat_clusters : list (tuples)
      Tuples giving the range of each cluster of saturated pixels in a
      spectrum. Note that w, z, sat, and composite clusters are 
      non-overlapping after processing.

  c_clusters: list (tuples)
      Tuples giving the range of each cluster of composite w-z pixels in a 
      spectrum. Note that w, z, and composite clusters are non-overlapping
      after processing.

  w_coeffs: dict (int -> tuple)
      Maps each water telluric pixel to a tuple containg the coeffcients
      in its linear regression model against the selected calibration 
      pixel. The tuple, t, represents the coefficients in the regression
      as y = t[0]*x + t[1].

  z_coeffs: dict (int -> tuple)
      Maps each water telluric pixel to a tuple containg the coeffcients
      in its linear regression model against airmass (see w_coeffs).
  """

  def __init__(self, order):
    self.order = order
    self.px_no = None
    self.spectra = {}
    self.l_cutoff_wv = None
    self.r_cutoff_wv = None
    self.w_PCCs = None
    self.w_tel = None
    self.w_clusters = []
    self.z_PCCs = None
    self.z_tel = None
    self.z_clusters = []
    self.s_tel = None
    self.s_clusters = []
    self.c_clusters = []
    self.w_coeffs = {}
    self.z_coeffs = {}

  def initialize_telluric_arrays(px_no):
    self.w_PCCs = np.zeros(px_no) + NULL_INT
    self.w_tel = np.zeros(px_no, dtype=bool)
    self.z_PCCs = np.zeros(px_no) + NULL_INT
    self.z_tel = np.zeros(px_no, dtype=bool)
    self.s_tel = np.zeros(px_no) + NULL_INT

class Spectrum_Data():

  """
  Stores the data associated with a file in a shard's wavelength range.

  Parameters
  ----------

  lin_x: array (float)
      Spectrum wavelength data

  log_y: array (float)
      Spectrum intensity data in log space

  z: float
      Spectrum airmass

  continuum: array (float)
      Blaze continuum

  Attributes
  ----------
  lin_x: array (float)
      (see parameters)

  log_y: array (float)
      (see parameters)

  z: float
      (see parameters)

  continuum: array (float)
      (see parameters)

  tel_lin_y: array (float)
      Telluric spectrum for the shard in lin space.

  div_lin_y: array (float)
      Spectrum after dividing through by tellurics in lin space.
  """
  
  def __init__(self, lin_x, log_y, z, continuum, uncertainty, snrs):
    self.lin_x = lin_x
    self.log_y = log_y
    self.z = z
    self.continuum = continuum
    self.uncertainty = uncertainty
    self.snrs = snrs
    self.px_no = None
    self.tel_lin_y = None
    self.div_lin_y = None
