import csv
import os

from . import db_indicies as dbi

def read_db(filename, read_calibrator_info=False):

    """
    Reads in telluric model database.
    """

    #1: Open database, create data container
    csv_file = open(filename, 'r')
    csv_reader = csv.reader(csv_file, delimiter=" ", quotechar="'")
    db = []
    order_wv_ranges = {}

    #2: Parse database header
    title_record = next(csv_reader)

    #3: Parse database wavelength ranages
    wavelength_records_title = next(csv_reader)
    wavelength_header_record = next(csv_reader)

    while True:

      record = next(csv_reader)

      # If record is main database header, break
      if record[dbi.ORD_IND] == "Telluric pixels":
        break

      order = int(record[dbi.ORD_IND])
      lo_wv = float(record[dbi.LO_WV_IND])
      hi_wv = float(record[dbi.HI_WV_IND])
    
      order_wv_ranges[order] = (lo_wv, hi_wv)

    #4: Parse database tellurics
    tellurics_header_record = next(csv_reader)

    while True:

        try:
          record = next(csv_reader)
        except StopIteration:
          break
      
        if len(record) < dbi.DB_RECORD_LEN or len(record) > dbi.DB_RECORD_LEN:
            raise Exception("Db record doesn't have {} fields.\n {}".format(dbi.DB_RECORD_LEN,
                                                                            record))

        try: 
            record[dbi.ORD_IND] = int(record[dbi.ORD_IND])
            record[dbi.PX_IND] = int(record[dbi.PX_IND])
            record[dbi.WV_IND] = float(record[dbi.WV_IND])
            record[dbi.PCC_IND] = float(record[dbi.PCC_IND])
            record[dbi.RM_IND] = float(record[dbi.RM_IND])
            record[dbi.RC_IND] = float(record[dbi.RC_IND])
            record[dbi.INT_IND] = float(record[dbi.INT_IND])
        except ValueError:
            raise Exception("Field in db record corrupt. Record:{}".format(record))

        db.append(record)
    return db, order_wv_ranges
    
