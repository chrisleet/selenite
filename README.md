# selenite
The SELENITE Telluric Modelling Code

## Code Directory
* `test_data`: contains data required to run SELENITE test cases
* `selenite`: the SELENITE code itself!
* `runtime`: Shell folder that stores runtime data artifacts.

## Programs
SELENITE's workflow works as follows: 
* `normalize_bstars.py`: A dataset of featureless B/A type stars are read in, preprocessed, and stored in easy to access datastructures.
* `calibrate_selenite.py`: A wavelength grid is taken from a provided science spectrum. The B/A stars are read, interpolated onto this wavelength grid, and a model for the tee lluric contribution to each pixel of the wavelength grid generated and stored in a db.
* `fit_selenite.py`: A science spectrum is provided. The depths of each of its calibration lines are taken and used to fit the telluric model generated in `calibrate_selenite.py` to it. The results are written out to the fits file.
* `plot_tellurics.py`: Courtesy function which takes a science spectrum after it has been augmented with tellurics and plots both the science spectrum and the tellurics.

## Installing SELENITE
1. Set up a virtual environment.

```python3 -m venv env```

2. Install dependencies.

```python3 -m pip install pyyaml```
```python3 -m pip install astropy```
```python3 -m pip install matplotlib```
```python3 -m pip install numpy```
```python3 -m pip install scipy```

That's it!

## Running the test case!
The SELENITE repository contains a science spectrum and ~200 normalized B star spectra as a test case. The test case can be run as follows.
1. Since the test B stars have already been normalized, there is no need to run `normalize_bstars.py`. We go right to building the telluric model using:

```python3 selenite/calibrate_selenite.py test_data/science_spectra/101501_180526.1086.fits runtime/dbs/test_db.csv selenite/config/calibrate_selenite_cfg.yml```

2. We then fit the telluric model to the science spectrum using:

```python3 selenite/fit_selenite.py test_data/science_spectra/101501_180526.1086.fits runtime/dbs/test_db.csv selenite/config/fit_selenite_cfg.yml```

3. Finally, the fitted model can be plotted by:

```python3 selenite/plot_tellurics.py -o 72 test_data/science_spectra/101501_180526.1086.fits```
