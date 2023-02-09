"""Create BrainVoyager VMR file."""

import bvbabel

OUTNAME = "/home/faruk/Git/bvbabel/test_data/temp_tests/default_bvbabel.vmr"

# -----------------------------------------------------------------------------
# Create VMR fiel with random intensity values
header, data = bvbabel.vmr.create_vmr()
bvbabel.vmr.write_vmr(OUTNAME, header, data)

print("Finished.")
