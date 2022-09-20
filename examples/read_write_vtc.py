"""Read and write BrainVoyager VTC (volume time course) file."""

import os
import bvbabel
from pprint import pprint

FILE = "/home/faruk/Documents/test_bvbabel/vtc/S01_run1_sc.vtc"

# =============================================================================
# Load vmr
header, data = bvbabel.vtc.read_vtc(FILE, rearrange_data_axes=False)

# See header information
pprint(header)

# Save VTC
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.vtc".format(basename)
bvbabel.vtc.write_vtc(outname, header, data, rearrange_data_axes=False)

print("Finished.")
