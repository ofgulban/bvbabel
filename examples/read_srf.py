"""Read Brainvoyager vtc and export nifti."""

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

print("Finished.")
