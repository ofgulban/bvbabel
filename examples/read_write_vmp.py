"""Read and write BrainVoyager VMP (volume map) file."""

import os
import bvbabel
import pprint

FILE = "/home/faruk/Documents/test_bvbabel/sub-01_ses-01_RightHand.vmp"

# =============================================================================
# Load vmr
header, data = bvbabel.vmp.read_vmp(FILE)

# See header information
pprint.pprint(header)

# Modify one map
data[..., 0] *= -1

# Write VMP
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.vmp".format(basename)
bvbabel.vmp.write_vmp(outname, header, data)

print("Finished.")
