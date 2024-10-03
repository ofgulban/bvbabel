"""Read NIFTI and plot event related averages for each ROI."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

NII_TC = "/Users/faruk/data/test-ERA/sub-08_task-amb_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF5c_sess-01_BBR_res2x_bvbabel_2D_VOI_TimeCourses.nii.gz"

# =============================================================================
# Step 1: Load nifti time course
nii = nb.load(NII_TC)
data = nii.get_fdata()

# Step 2: Determine necessary information
nr_timepoints = data.shape[0]
nr_voxels = data.shape[1]
print(f"  Nr. timepoints {nr_timepoints}")
print(f"  Nr. voxels {nr_voxels}")

# Step 3: Order by mean intensity
data_mean = np.mean(data, axis=0)
idx = np.argsort(data_mean)
# idx = np.repeat(idx[None, :], nr_timepoints, axis=0)
temp = data[:, idx]

basename = NII_TC.split(os.extsep, 1)[0]
outname = "{}_TEST.nii.gz".format(basename)
img = nb.Nifti1Image(temp, affine=nii.affine)
nb.save(img, outname)

print(idx.shape)
