"""Create BrainVoyager VTC file."""

import bvbabel

OUTNAME = "/home/faruk/Documents/test_bvbabel/vtc/default_bvbabel.vtc"

# -----------------------------------------------------------------------------
header, data = bvbabel.vtc.create_vtc()
bvbabel.vtc.write_vtc(OUTNAME, header, data)

print("Finished.")
