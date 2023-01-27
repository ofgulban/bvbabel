"""Create BrainVoyager SDM file."""

import bvbabel

OUTNAME = "/home/faruk/Git/bvbabel/test_data/temp.sdm"

# -----------------------------------------------------------------------------
header, data = bvbabel.sdm.create_sdm()
bvbabel.sdm.write_sdm(OUTNAME, header, data)

print("Finished.")
