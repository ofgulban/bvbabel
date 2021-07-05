"""Read Brainvoyager vtc and export nifti."""

import numpy as np
import bvbabel
from pprint import pprint

FILE = "/home/faruk/Documents/test_bvbabel/gtc/gtc_test.gtc"
OUTNAME = "/home/faruk/Documents/test_bvbabel/gtc/gtc_test_bvbabel.gtc"

# =============================================================================
# Load vmr
header, data = bvbabel.gtc.read_gtc(FILE)

# See header information
pprint(header)

# Invert voxel intensities
data = (data * -1) + np.max(data)

# Export nifti
bvbabel.gtc.write_gtc(OUTNAME, header, data)

print("Finished.")
