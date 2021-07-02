"""Read Brainvoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

FILE = "/home/faruk/Documents/test_bvbabel/sub-01_ses-01_RightHand.vmp"
OUTNAME = "/home/faruk/Documents/test_bvbabel/sub-01_ses-01_RightHand_bvbabel.vmp"

# =============================================================================
# Load vmr
header, data = bvbabel.vmp.read_vmp(FILE)

# See header information
pprint.pprint(header)

# Modify one map
data[..., 0] *= -1

# Write VMP
bvbabel.vmp.write_vmp(OUTNAME, header, data)

print("Finished.")
