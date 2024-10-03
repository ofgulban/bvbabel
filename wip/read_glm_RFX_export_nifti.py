"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

FILE = "/mnt/e/WB-MotionQuartet/derivatives/TEST/task-phy_VTC_N-18_RFX_PT_AR-2_MSK-brainmask_MNI_pt6.glm"

# =============================================================================
# Load vmr
header, data_R2, data_SS, data_beta, data_SS_XiY, data_meantc, data_arlag = bvbabel.glm.read_glm(FILE)

# See header information
pprint.pprint(header)

# -----------------------------------------------------------------------------
# Export nifti
basename = FILE.split(os.extsep, 1)[0]

# Beta values
outname = "{}_beta_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(data_beta, affine=np.eye(4))
nb.save(img, outname)

print("Finished.")
