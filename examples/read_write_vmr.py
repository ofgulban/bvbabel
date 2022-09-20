"""Read and write BrainVoyager VMR (anatomical MRI) file."""

import os
import bvbabel

FILE = "/home/faruk/Documents/test_bvbabel/sub-01_MNI.vmr"

# =============================================================================
# Load vmr
header, data_img = bvbabel.vmr.read_vmr(FILE)

# Invert intensities
data_img = (data_img * -1) + 225

# Print header nicely
for key, value in header.items():
    print(key, ":", value)

# Write VMR
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.vmr".format(basename)
bvbabel.vmr.write_vmr(outname, header, data_img)

header2, data_img2 = bvbabel.vmr.read_vmr(outname)

# Print header nicely
for key, value in header2.items():
    print(key, ":", value)

print("Finished.")
