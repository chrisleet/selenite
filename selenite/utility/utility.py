import numpy as np

def coadd_spectrum(shard):

    """
    Coadds each spectrum in shard.
    """

    coadd_x = np.zeros(shard.px_no)
    coadd_y = np.zeros(shard.px_no)
    cnt = 0
    for key, spectrum in shard.spectra.items():
        coadd_x += spectrum.lin_x
        coadd_y += spectrum.log_y
        cnt += 1
    coadd_x /= cnt
    coadd_y /= cnt
    return (coadd_x, coadd_y)

