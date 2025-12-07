"""Read BrainVoyager VTC and export NIfTI."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

FILE = "/Users/faruk/data/temp-GLM/sub-06.vtc"

# =============================================================================
# Load vtc
header, data = bvbabel.vtc.read_vtc(FILE, rearrange_data_axes=False)

# See header information
pprint(header)

# Transpose axes
data = np.transpose(data, [0, 2, 1, 3])
# Flip axes
data = data[::-1, ::-1, ::-1, :]

# Export nifti
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.nii.gz".format(basename)

# Create affine
affine = np.eye(4) * header["VTC resolution relative to VMR (1, 2, or 3)"]

# -----------------------------------------------------------------------------
# (Optional) Insert translation values when necessary
# NOTE: These need to be figured out for each necessary transpose and flip
# -----------------------------------------------------------------------------
# TARGET_VMR_DIMENSION = 256 # Often 256, but can also be an integer multiple
# affine[1, 3] = TARGET_VMR_DIMENSION - header["XEnd"] + 1.5
# affine[2, 3] = TARGET_VMR_DIMENSION - header["YEnd"] + 1.5
# affine[0, 3] = TARGET_VMR_DIMENSION - header["ZEnd"] + 1.5

# -----------------------------------------------------------------------------
# Save
img = nb.Nifti1Image(data, affine=affine)
nb.save(img, outname)

print("Finished.")
