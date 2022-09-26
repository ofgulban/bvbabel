"""Read BrainVoyager vtc and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

FILE = "/home/faruk/Documents/test_bvbabel/vtc_test.vtc"

# =============================================================================
# Load vmr
header, data = bvbabel.vtc.read_vtc(FILE)

# See header information
pprint(header)

# Export nifti
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(data, affine=np.eye(4))
nb.save(img, outname)

print("Finished.")
