"""Read Brainvoyager vmr and export nifti."""

import bvbabel
import numpy as np

FILE = "/home/faruk/Documents/test_bvbabel/vmr/S07_SES1_T1_divPD_IIHC_pt5_TAL_edit.vmr"
OUT = "/home/faruk/Documents/test_bvbabel/vmr/poh.vmr"

# Load vmr
header, data_img = bvbabel.vmr.read_vmr(FILE)

# Print header nicely
for key, value in header.items():
    print(key, ":", value)

# Write VMR
bvbabel.vmr.write_vmr(header, data_img, OUT)

header2, data_img2 = bvbabel.vmr.read_vmr(OUT)
# Print header nicely
for key, value in header2.items():
    print(key, ":", value)

print("Finished.")
