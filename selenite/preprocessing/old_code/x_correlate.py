import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.interpolation import shift
from scipy.signal import correlate

from ..data_containers import shard as shi
from ..load_store import db_indicies as dbi

def x_correlate(shards, template_spectrum, should_xcorr):

    """
    XCorrelates each spectrum with template_spectrum if should_xcorr true.
    """
    
    if not should_xcorr:
        return


    for shard in shards.values():
        for spectrum in shard.spectra.values():
            spectrum.log_y[spectrum.log_y > -0.02] = 0

    for shard in shards.values():
        std_log_y = shard.spectra[template_spectrum].log_y
        for filename, spectrum in shard.spectra.items():
            offset = np.argmax(correlate(std_log_y, spectrum.log_y)) - (len(std_log_y) - 1)
            spectrum.log_y = shift(spectrum.log_y, offset, cval=0)
        
        fig = plt.figure()
        plt.plot(shard.spectra[template_spectrum].log_y, marker="X", color="gold", zorder=2)
        plt.plot(shard.spectra[template_spectrum].log_y, color="gold", zorder=2)
        for spectrum in shard.spectra.values():
            plt.plot(spectrum.log_y, zorder=1)
        plt.show()




def x_correlate_db(cal_pxs, shards, db, config):

    """
    XCorrelate the telluric model with the spectrum on the calibration pxs.
    """
        
    best_shift = -config["x_corr_shift"]
    best_SSE = float('inf')
    for shift in range(-config["x_corr_shift"], config["x_corr_shift"]+1):
        SSE = 0
        SSEs = {}
        r_ys, s_ys = [], []

        i = 0
        for r in db:
            r_order = r[dbi.ORD_IND]
            r_x = r[dbi.PX_IND] + shift
            r_y = r[dbi.INT_IND]
            if (r_order, r[dbi.PX_IND]) in cal_pxs and r[dbi.CLS_IND] == "w":
                for shard in shards.values():
                    if shard.order == r_order and shard.lo_px <= r_x and r_x < shard.hi_px:
                        s_y = iter(shard.spectra.values()).next().log_y[r_x - shard.lo_px]
                        # Note: Because log values are negative, r_y - s_y is positive when
                        # the science spectrum s_y is deeper than the telluric spectrum r_y
                        DIFF_LIM = 0.1 # Cap r_y - s_y to DIFF_LIM
                        if r_y - s_y  > DIFF_LIM:
                            SSE += DIFF_LIM
                        else:
                            SSE += abs(r_y - s_y)
                        SSEs[(r_order, r[dbi.PX_IND])] = abs(r_y - s_y)

                        r_ys.append(r_y)
                        s_ys.append(s_y)

        #print "SSEs:{}".format(SSEs)
        print("shift:{} SSE:{}, best_shift:{}, best_SSE:{}".format(shift, SSE, best_shift, best_SSE))
        #plot_xcorr_step(s_ys, r_ys, shift)

        if SSE < best_SSE:
            best_shift = shift
            best_SSE = SSE
    
    return best_shift   
