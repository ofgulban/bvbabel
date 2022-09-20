"""Read and write BrainVoyager GTC (grid time course) file."""

import os
import numpy as np
import bvbabel
from pprint import pprint

FILE = "/home/faruk/Documents/test_bvbabel/gtc/gtc_test.gtc"

# =============================================================================
# Load vmr
header, data = bvbabel.gtc.read_gtc(FILE)

# See header information
pprint(header)

# Invert voxel intensities
data = (data * -1) + np.max(data)

# Export nifti
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.gtc".format(basename)
bvbabel.gtc.write_gtc(outname, header, data)

print("Finished.")
