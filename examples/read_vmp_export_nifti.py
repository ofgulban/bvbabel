"""Read Brainvoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

FILE = "/home/faruk/Documents/test_bvbabel/vmp/sub-01_ses-01_RightHand.vmp"

# Load vmr
header, data = bvbabel.vmp.read_vmp(FILE)

# -----------------------------------------------------------------------------
# See header information
pprint.pprint(header)

# -----------------------------------------------------------------------------
# Export nifti
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(data, affine=np.eye(4))
nb.save(img, outname)
