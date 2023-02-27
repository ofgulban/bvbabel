"""Read and write BrainVoyager FMR (functional MRI data) file."""

import os
import bvbabel
from pprint import pprint

FILE = "/home/faruk/Documents/test_bvbabel/S01_RUN_01_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_FLIRT_TU.fmr"

# =============================================================================
# Load FMR (and its paired STC file)
header, data = bvbabel.fmr.read_fmr(FILE)

# See header information
pprint(header)

# Save FMR (and its paired STC file)
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.fmr".format(basename)
bvbabel.fmr.write_fmr(outname, header, data)

print("Finished.")
