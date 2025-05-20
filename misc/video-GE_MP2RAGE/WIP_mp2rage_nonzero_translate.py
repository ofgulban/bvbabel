"""Adjust data range of GE 7 T MP2RAGE UNI images."""

import os
import nibabel as nb
import numpy as np

FILE = "/Users/faruk/data/temp-hugo_caffarati/faruk/MP2RAGE_UNI.nii.gz"

# =============================================================================
# Load nifti
nii = nb.load(FILE)
data = np.asarray(nii.dataobj)

# Non-zero shift
idx = data != 0
data[idx] -= data.min()

# Save
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(data, affine=nii.affine, header=nii.header)
nb.save(img, outname)

print("Finished.")
