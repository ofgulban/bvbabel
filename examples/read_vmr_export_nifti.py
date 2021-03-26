"""Read Brainvoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel

FILE = "/home/faruk/Documents/test_bvbabel/T1.vmr"

# Load vmr
header, data = bvbabel.vmr.read_vmr(FILE)

# Print header nicely
for key, value in header.items():
    print(key, ":", value)

# Export nifti
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(data, affine=np.eye(4))
nb.save(img, outname)
