"""Read Brainvoyager vmr and export nifti."""

import bvbabel
import numpy as np

FILE = "/home/faruk/Documents/test_bvbabel/sub-01_MNI.vmr"
OUTNAME = "/home/faruk/Documents/test_bvbabel/sub-01_MNI_bvbabel.vmr"

# =============================================================================
# Load vmr
header, data_img = bvbabel.vmr.read_vmr(FILE)

# Invert intensities
data_img = (data_img * -1) + 225

# Print header nicely
for key, value in header.items():
    print(key, ":", value)

# Write VMR
bvbabel.vmr.write_vmr(OUTNAME, header, data_img)

header2, data_img2 = bvbabel.vmr.read_vmr(OUTNAME)
# Print header nicely
for key, value in header2.items():
    print(key, ":", value)

print("Finished.")
