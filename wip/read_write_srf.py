"""Read Brainvoyager srf and export Wavefront obj file."""

import os
import bvbabel
from pprint import pprint

FILE = "/home/faruk/Documents/temp_bvbabel_smp/S02_LH_HIRES_SPH.srf"

# =============================================================================
# Load vmr
header, mesh_data = bvbabel.srf.read_srf(FILE)

# See header information
pprint(header)

# Save SRF
# TODO: Resolve black color issue
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.srf".format(basename)
bvbabel.srf.write_srf(outname, header, mesh_data)

print("Finished.")
