"""Create BrainVoyager VMP file."""

import bvbabel

OUTNAME = "/home/faruk/Git/bvbabel/test_data/temp_tests/default_bvbabel.vmp"

# -----------------------------------------------------------------------------
# Create VMP fiel with random intensity values
header, data = bvbabel.vmp.create_vmp()
bvbabel.vmp.write_vmp(OUTNAME, header, data)

print("Finished.")
