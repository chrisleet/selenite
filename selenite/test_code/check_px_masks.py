import numpy as np

import expres.selenite.load_store.load_px_masks as load_px_masks

def check_px_masks():

  px_masks = load_px_masks.load_px_masks("all")
  for order in np.arange(38, 86):
    px_mask_len = None
    for px_mask_name, px_mask in px_masks.items():
      px_mask_len = np.sum(px_mask[order])
      print(px_mask_name, order, px_mask_len)

if __name__ == "__main__":
  check_px_masks()
      
