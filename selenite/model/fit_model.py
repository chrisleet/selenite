import matplotlib.pyplot as plt
import numpy as np

from data_containers import shard as shi
from load_store import db_indicies as dbi


def get_z(shards):

    """
    Get the science spectrum's airmass, z.
    """

    return next(iter(next(iter(shards.values())).spectra.values())).z

def get_mu(cal_pxs, shards, db, config):

    """
    Get the depth of the science spectrum's water calibration line, mu.

    The water calibration line may be blended with a stellar line, making
    it difficult to measure directly. However, since all water lines grow
    proportionally to each other, we can experiment by scaling the water
    telluric spectrum by different values of mu and examining its fit to
    the science spectrum's water tellurics.

    Fitting to blended telluric lines, however, can throw off the overall
    fit. To remove blended calibration lines, we fit the telluric spectrum
    to the provided set of telluric lines, and then remove all lines whose
    error is an outlier (beyond 1.5 std dev away from the mean error.) 

    This process is iterated until no line's fit is 1.5 std dev from
    the mean error or until all lines are less than MIN_RNG away from the
    mean error.
    """

    lo_range = config["lo_mu"] # The low end of range of mu to search
    hi_range = config["hi_mu"] # The high end of range of mu to search
    epsilon = config["mu_epsilon"] # When mu's error is less than this value, stop search
    MIN_RNG = 0.01  # When all points have less than this fitting error, stop iteratively fitting
    STD_RNG = 3 # Points with error more than STD_RNG std dev from the mean error and considered
                  # anomolous and removed.

    # Convert cal_pxs to measured_cal_pxs format
    measured_cal_pxs = []
    for order, px in cal_pxs:
        measured_cal_pxs.append((order, px))

    while True:
        
        mu, mu_errs = minimize_mu_err(measured_cal_pxs, lo_range, hi_range, 
                                      epsilon, shards, db)

        mean, std = np.mean(list(mu_errs.values())), np.std(list(mu_errs.values()))
        hi_threshold = mean+1.5*max(std,MIN_RNG)
        lo_threshold = mean-1.5*max(std,MIN_RNG)

        #print "mu_errs:{}".format(sorted( ((v,k) for k,v in mu_errs.iteritems()), reverse=True))
        #print "std:{}".format(std)
        #print "+/- 1:{},{}".format(mean-std, mean+std)
        #print "+/- 1.5:{},{}".format(mean-1.5*std, mean+1.5*std)
        #print "+/- 2:{},{}".format(mean-2*std, mean+2*std)
        #print "+/- 3:{},{}".format(mean-3*std, mean+3*std)
        #print "threshold:{},{}".format(lo_threshold, hi_threshold)

        new_measured_cal_pxs = [cal_px for cal_px in list(mu_errs.keys()) 
                                if mu_errs[cal_px] < hi_threshold 
                                and mu_errs[cal_px] > lo_threshold]

        #print "cal_pxs:{}".format(measured_cal_pxs)
        #print "new_cal_pxs:{}".format(new_measured_cal_pxs)
        if config["plot_fspec_fitting_steps"]:
            plot_mu_spectrum(measured_cal_pxs, mu, db, shards)

        if set(measured_cal_pxs) == set(new_measured_cal_pxs):
            break

        measured_cal_pxs = new_measured_cal_pxs

    return mu

def minimize_mu_err(measured_cal_pxs, lo_range, hi_range, epsilon, shards, db):

    """
    Find mu that minimizes error between model and spectrum cal px.

    Conducts binary search to find a value for mu that minimizes the mean error
    between the telluric model and the science spectrum's calibration pixels.
    """
    
    # 1: Perform binary search between hi_range and lo_range to find a mu that best fits 
    # calibration pixels
    while hi_range - lo_range > epsilon:

        # 2: Pick mu as the center of the current range of mus, and find the error of its 
        # corresponding telluric spectrum at each calibrator pixel
        mu = (hi_range + lo_range) / 2.0
        mu_errs_dict = find_mu_errs(measured_cal_pxs, mu, db, shards)

        # 3: If err is positive, mu is too large. Search for mu in the inverval (lo_range,
        # current mu). If err is negative, mu is too small. Search for mu in the interval
        # (current mu, hi_range)
        if np.mean(list(mu_errs_dict.values())) > 0:
            hi_range = mu
        else:
            lo_range = mu

    return mu, mu_errs_dict

def find_mu_errs(measured_cal_pxs, mu, db, shards):

    """
    Water telluric model with PVW mu's error with a science spectrum.

    Build a water telluric model with PVW mu and calculate the signed, squared
    error of each of the science spectrum's calibration pixels with this model.
    Returns a dict mapping each calibration pixel to its error.
    """

    mu_errs_dict = {}
    for r in db:

        # 1: For each record, extract its order, px, and intensity with mu
        r_order = r[dbi.ORD_IND]
        r_x = r[dbi.PX_IND]
        r_y = r[dbi.RM_IND] * mu + r[dbi.RC_IND]

        # 2: Check if record is a calibrator (check unshifted pixel since calibrators
        # selected from telluric spectrum.)
        if (r_order, r[dbi.PX_IND]) in measured_cal_pxs and r[dbi.CLS_IND] == "w":

            # 3: If it is, find the corresponding pixel in shards, and calculate the
            # telluric spectrum's error at that pixel with mu
            for shard in shards.values():
                if shard.order == r_order:
                    s_y = next(iter(shard.spectra.values())).log_y[r_x]
                    mu_errs_dict[(r_order, r[dbi.PX_IND])] = (r_y - s_y)

    return mu_errs_dict


def plot_mu_spectrum(measured_cal_pxs, mu, db, shards):

    """
    Overplots the science and telluric spectrum for each given mu.

    Spectrum are plotted with calibration pixels highlighted and errors 
    measured shown above them.
    """

    for shard in shards.values():

        # 1: Get the science spectrum.
        spectrum = next(iter(shard.spectra.values()))

        # 2: Compute the telluric spectrum associated with mu and the index of any calibration
        # pixel in the shard.
        db_spectrum = np.ones(len(spectrum.log_y))
        cal_px_inds = []

        for r in db:
            
            # 2a: Don't plot non-water lines
            if r[dbi.CLS_IND] != "w":
                continue
            
            # 2b: Calculate the intensity of each telluric pixel in the order
            r_x = r[dbi.PX_IND]
            if r[dbi.ORD_IND] == shard.order:
                db_spectrum[r_x] = np.exp(r[dbi.RM_IND] * mu + r[dbi.RC_IND])

                # 2c: If telluric pixel was a calibration pixel, record its ind
                if (r[dbi.ORD_IND], r[dbi.PX_IND]) in measured_cal_pxs:
                    cal_px_inds.append(r_x)
        
        cal_px_inds = np.array(cal_px_inds)

        # 3: Plot telluric spectrum and errors against science spectrum
        fig = plt.figure(facecolor = 'white')

        # 3a: Plot CHIRON and telluric spectrum
        plt.plot(spectrum.lin_x, np.exp(spectrum.log_y), color='purple', 
                 label='CHIRON Spectrum')
        plt.plot(spectrum.lin_x, db_spectrum, label='Telluric Spectrum')

        #3b: Highlight calibration pixels
        if len(cal_px_inds) > 0:
            plt.scatter(spectrum.lin_x[cal_px_inds], 
                        np.exp(spectrum.log_y)[cal_px_inds], color="red")
            plt.scatter(spectrum.lin_x[cal_px_inds], db_spectrum[cal_px_inds], 
                        color="red", label="Calibration px")

        # 3c: Format chart
        plt.title("Order {}, mu:{} telluric model ".format(shard.order, mu))
        plt.xlabel("Wavelength (Angstroms)")
        plt.ylabel("Signal strength")
        plt.tight_layout()
        plt.legend()
        plt.show()
