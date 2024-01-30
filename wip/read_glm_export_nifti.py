"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

FILE = "/Users/faruk/data/temp-GLM/test2.glm"

# =============================================================================
# Load vmr
header, data_R2, data_SS, data_beta, data_SS_XiY, data_meantc, data_arlag = bvbabel.glm.read_glm(FILE)

# See header information
pprint.pprint(header)

# -----------------------------------------------------------------------------
# Export nifti
basename = FILE.split(os.extsep, 1)[0]

# Multiple regression R value
outname = "{}_R2_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(data_R2, affine=np.eye(4))
nb.save(img, outname)

# Sum of squares values
outname = "{}_SS_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(data_SS.astype(np.int32), affine=np.eye(4))
nb.save(img, outname)

# Beta values
outname = "{}_beta_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(data_beta, affine=np.eye(4))
nb.save(img, outname)

# Sum-of-squares indicating the covariation of each predictor with the time 
# course (SS_XiY). these values may be ignored for custom processing.
outname = "{}_XY_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(data_SS_XiY, affine=np.eye(4))
nb.save(img, outname)

# Mean time course
outname = "{}_meantc_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(data_meantc, affine=np.eye(4))
nb.save(img, outname)

# Auto-regression lag value
outname = "{}_atrlag_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(data_arlag, affine=np.eye(4))
nb.save(img, outname)

print("Finished.")
