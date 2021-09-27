"""Create Brainvoyager VTC file."""

import bvbabel

OUTNAME = "/home/faruk/Documents/test_bvbabel/vtc/default_bvbabel.vtc"

# -----------------------------------------------------------------------------
header, data = bvbabel.vtc.generate_vtc()
bvbabel.vtc.write_vtc(OUTNAME, header, data)

print("Finished.")
