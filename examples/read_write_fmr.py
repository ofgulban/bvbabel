"""Read and write BrainVoyager FMR (functional MRI data) file."""

import os
import bvbabel

FILE = "/home/faruk/Documents/test_bvbabel/fmr/nifti_converted.fmr"

# =============================================================================
# Load FMR (and its paired STC file)
header, data = bvbabel.fmr.read_fmr(FILE)

# Save FMR (and its paired STC file)
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.fmr".format(basename)
bvbabel.fmr.write_fmr(outname, header, data)

print("Finished.")
