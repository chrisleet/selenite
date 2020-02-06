import os

import argparse

def has_valid_ext(filename, valid_exts):

    """
    Throws parser error if input file's ext isn't in valid_exts.
    """

    base, ext = os.path.splitext(filename)
    if ext.lower() not in valid_exts:
        raise argparse.ArgumentTypeError('File extension must be in:{}'.format(valid_exts))
    return filename

def is_csv_file(filename):
    return has_valid_ext(filename, [".csv"])

def is_fits_file(filename):
    return has_valid_ext(filename, [".fits"])

def is_yaml_file(filename):
    return has_valid_ext(filename, [".yml"])
