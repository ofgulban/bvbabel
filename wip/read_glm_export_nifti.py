"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

FILE = "/home/faruk/Documents/temp_bvbabel_glm/BOLD_whole_brain_GLM.glm"

# =============================================================================
# Load vmr
header, data_R2, data_SS, data_beta, data_fitted, data_arlag = bvbabel.glm.read_glm(FILE)

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

# Fitted data after regression
outname = "{}_fitted_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(data_beta, affine=np.eye(4))
nb.save(img, outname)

# Auto-regression lag value
outname = "{}_atrlag_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(data_beta, affine=np.eye(4))
nb.save(img, outname)

print("Finished.")
