"""Read and write BrainVoyager MTC (mesh time course) file."""

import os
import bvbabel
from pprint import pprint

FILE = "/home/faruk/Documents/test_bvbabel/mtc/sub-test03.mtc"

# =============================================================================
# Load vmr
header, data = bvbabel.mtc.read_mtc(FILE)

# See header information
pprint(header)

# Save MTC
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.mtc".format(basename)
bvbabel.mtc.write_mtc(outname, header, data)

print("Finished.")
