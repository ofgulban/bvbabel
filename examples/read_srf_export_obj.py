"""Read Brainvoyager srf and export Wavefront obj file."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

FILE = "/home/faruk/Documents/test_bvbabel/SRF/surface_mesh.srf"

# =============================================================================
# Load vmr
header, vtx, vtx_normals, faces, vtx_colors, vtx_neighbors = bvbabel.srf.read_srf(FILE)

# See header information
pprint(header)

np.unique(faces).max()
np.unique(faces).min()

print("Writing OBJ file...")
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.obj".format(basename)
bvbabel.obj.write_obj(outname, vtx, vtx_normals, faces)

print("Finished.")
