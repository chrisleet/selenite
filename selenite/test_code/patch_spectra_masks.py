def patch_spectra_masks():

  in_f_name = "/home/chrisleet/astronomy/data/epoch_masks/epoch1_mask.txt"
  out_f_name = "/home/chrisleet/astronomy/data/epoch_masks/patched_epoch1_mask.txt"

  in_f = open(in_f_name, "r")
  out_f = open(out_f_name, "w+")

  lines_84 = []

  for line in in_f:

    px, order, val = line.split()
    px, order, val = int(px), int(order), int(val)

    if order == 83:
      continue

    if order == 84:
      lines_84.append(line)
      line = line[:7] + "3" + line[8:]

    if order == 85 and px == 0:
      for line_84 in lines_84:
        out_f.write(line)

    out_f.write(line)

def patch_spectra_masks_2():

  
  in_f_name = "/home/chrisleet/astronomy/data/epoch_masks/epoch4_mask.txt"
  out_f_name = "/home/chrisleet/astronomy/data/epoch_masks/patched_epoch4_mask.txt"

  in_f = open(in_f_name, "r")
  out_f = open(out_f_name, "w+")

  lines_85 = []
  
  left_mask_px = None
  right_mask_px = None
  left_of_data = True
  in_data = False
  
  for line in in_f:

    px, order, val = line.split()
    px, order, val = int(px), int(order), int(val)

    if order == 85:
      lines_85.append(line)

      if val == 1 and left_of_data:
        left_mask_px = px
        left_of_data = False
        in_data = True
      
      elif val == 0 and in_data:
        right_mask_px = px-1
        in_data = False

    else:
      out_f.write(line)

  right_hand_delta = 500

  for line in lines_85:

    px, order, val = line.split()
    px, order, val = int(px), int(order), int(val)

    if order == 85 and px > right_mask_px - right_hand_delta and px <= right_mask_px:
      line = line[:10] + " 0" + line[12:]

    out_f.write(line)
    

  print("left_mask_px", left_mask_px)
  print("right_mask_px", right_mask_px)

  in_f.close()
  out_f.close()

if __name__ == "__main__":
  patch_spectra_masks_2()
    
