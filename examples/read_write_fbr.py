"""Read and write BrainVoyager FBR (diffusion weighted data: fiber reconstruction) file."""

import os
import bvbabel
from pprint import pprint

FILE = "/Users/hester_1/Progprojs/Python/2024/fbr/testvoi_DWI_b3000_PA_ACPC_132dirs_11x0_masked.fbr"

# =============================================================================
# Load FBR
header, data = bvbabel.fbr.read_fbr(FILE)

# See header information
pprint(header)

# Save FBR
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.fbr".format(basename)
bvbabel.fbr.write_fbr(outname, header, data)

print("Finished.")
