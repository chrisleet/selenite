import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

def print_chi_sq(shards, show=False):

    if not show:
        return

    total_unaff_summands = []
    total_aff_summands = []
    total_aff_r = []

    for shard in shards.values():
        
        spectrum = next(iter(shard.spectra.values()))

        unaff_summands, aff_summands = [], []
        unaff_r, aff_r = [], []

        # Settings
        pipeline_err = 0.0075
        no_obvs = 3.0
        scale_factor = 1.0

        for wv, x, mu in zip(spectrum.lin_x, spectrum.tel_lin_y, np.exp(spectrum.log_y)):
            sigma = (pipeline_err * scale_factor / np.sqrt(no_obvs * x))
            if x == 1.0: # and abs(mu - 1.0) < 0.02:
                unaff_summands.append(float(x-mu)**2 / sigma**2)
                #unaff_r.append(abs((x/mu) - 1.0)*100)
            elif x > -1.0 and abs(x - mu) < 0.03:
                aff_summand = float(x-mu)**2 / sigma**2
                #aff_summands.append(aff_summand)
                if aff_summand < 1000:
                    print("wv:{}, x:{}, mu:{}, sigma:{}, summ{}".format(wv, x, mu, sigma, aff_summand))
                    aff_summands.append(aff_summand)
                else:
                    print("wv:{}, x:{}, mu:{}, sigma:{}, summ{}".format(wv, x, mu, sigma, aff_summand))
                    #aff_summands.append(aff_summand)
                aff_r.append(abs(x/mu - 1.0)*100)

        if shard.order == 12:
            total_unaff_summands += unaff_summands
            total_aff_summands += aff_summands
            total_aff_r += aff_r
        

        #print "order:{}".format(shard.order)
        #print "unaff_chi_sq:{}".format(np.sum(unaff_summands) / (len(unaff_summands)-1))
        #print "aff_chi_sq:{}".format(np.sum(aff_summands) / (len(aff_summands)-1))

        #fig = plt.figure(facecolor="white")
        #n, bins, patches = plt.hist(unaff_summands, histedges_equalN(unaff_summands, 10), normed=True)
        #plt.show()

        #print "unaff_r:{}, aff_r:{}".format(np.mean(unaff_r), np.mean(aff_r))
        #print "unaff_std:{}, aff_std:{}".format(np.std(unaff_summands), np.std(aff_summands))

    print("chi sq statistics")
    print("-----------------")
    print("total unaff_chi_sq:{}".format(np.sum(total_unaff_summands) / (len(total_unaff_summands)-1)))
    print("# aff_summands:{}".format(len(total_aff_summands)))
    print("total aff_chi_sq:{}".format(np.sum(total_aff_summands) / (len(total_aff_summands)-1)))
    print("-----------------")

    print("residual statistics")
    print("-------------------")
    print("av residual from unity:{}".format(np.mean(aff_r)))
    print("-------------------")
