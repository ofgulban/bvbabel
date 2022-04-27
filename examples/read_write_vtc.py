"""Read Brainvoyager vtc and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

FILE = "/home/faruk/Documents/test_bvbabel/vtc_test.vtc"
OUTNAME = "/home/faruk/Documents/test_bvbabel/vtc_test_bvbabel.vtc"

# =============================================================================
# Load vmr
header, data = bvbabel.vtc.read_vtc(FILE)

# See header information
pprint(header)

# Invert voxel intensities
data = (data * -1) + np.max(data)

# Save VTC
bvbabel.vtc.write_vtc(OUTNAME, header, data)

print("Finished.")
