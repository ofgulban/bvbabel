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
img = nb.Nifti1Image(data, affine=np.eye(4))
nb.save(img, outname)

print("Finished.")
