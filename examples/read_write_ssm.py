"""Read and write BrainVoyager SSM (surface to surface map) file."""

import os
import bvbabel
from pprint import pprint

FILE = "/Users/faruk/data/temp-for_mesh_figure/TEST-BVBABEL/default.ssm"

# =============================================================================
# Load vmr
header, data_ssm = bvbabel.ssm.read_ssm(FILE)

# See header information
pprint(header)

# Save SMP
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.ssm".format(basename)
bvbabel.ssm.write_ssm(outname, header, data_ssm)

print("Finished.")
