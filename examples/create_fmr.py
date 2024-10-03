"""Create BrainVoyager FMR file."""

import bvbabel

OUTNAME = "/Users/faruk/Documents/test-bvbabel/default_bvbabel.fmr"

# -----------------------------------------------------------------------------
header, data = bvbabel.fmr.create_fmr()
bvbabel.fmr.write_fmr(OUTNAME, header, data)

print("Finished.")
