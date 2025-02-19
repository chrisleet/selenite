from data_containers import shard as shi

###########
# Globals #
###########

# Indices of calibrator lines in config file
ADDR_IND = 0
PX_IND = 1

def get_calibrators(science_spectrum_type, config):

    """
    Saves the calibrator pixels given in the config file in the form (order, px).
    """

    if science_spectrum_type in ["CHIRON_CSV", "CHIRON_FITS"]:
        spectrograph = "CHIRON"
    elif science_spectrum_type in ["EXPRES_FITS"]:
        spectrograph = "EXPRES"
    else:
        raise Exception("Did not recognize science spectrum type to get calibrator for.")


    cal_pxs = []
    for calibrator in config["calibrators"][spectrograph]:
        cal_pxs.append((calibrator[ADDR_IND][shi.ORD_IND],
                       calibrator[ADDR_IND][shi.LOPX_IND] + calibrator[PX_IND]))
    return cal_pxs
