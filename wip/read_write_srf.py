"""Read BrainVoyager srf and export Wavefront obj file."""

import os
import bvbabel
from pprint import pprint

FILE = "/Users/faruk/data/temp-for_mesh_figure/test-SRF/sub-test02_left_hemisphere.srf"

# =============================================================================
# Load vmr
header, mesh_data = bvbabel.srf.read_srf(FILE)

# See header information
pprint(header)

# (Example) Make all colors red
pprint(mesh_data["vertex colors"][:5, :])
mesh_data["vertex colors"][:, 0] = 0  # Blue
mesh_data["vertex colors"][:, 1] = 0  # Green
mesh_data["vertex colors"][:, 2] = 255  # Red
pprint(mesh_data["vertex colors"][:5, :])

# Save SRF
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.srf".format(basename)
bvbabel.srf.write_srf(outname, header, mesh_data)

print("Finished.")
