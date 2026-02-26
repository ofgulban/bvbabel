"""Create BrainVoyager SSM (surface to surface map) file."""

import bvbabel

OUTNAME = "/Users/faruk/data/temp-for_mesh_figure/TEST-BVBABEL/default.ssm"

# -----------------------------------------------------------------------------
# Create SSM file with random intensity values
header, data = bvbabel.ssm.create_ssm()
bvbabel.ssm.write_ssm(OUTNAME, header, data)

print("Finished.")
