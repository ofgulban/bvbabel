"""Read Brainvoyager srf and export Wavefront obj file."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

FILE = "/home/faruk/Documents/test_bvbabel/SRF/surface_mesh.srf"

# =============================================================================
# Load vmr
header, mesh_data = bvbabel.srf.read_srf(FILE)

# See header information
pprint(header)

print("Writing OBJ file...")
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.obj".format(basename)
bvbabel.obj.write_obj(outname, mesh_data["vertices"],
                      mesh_data["vertex normals"],
                      mesh_data["faces"])

print("Finished.")
