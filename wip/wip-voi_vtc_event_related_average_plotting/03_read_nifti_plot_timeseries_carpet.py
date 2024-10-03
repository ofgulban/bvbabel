"""Read NIFTI and plot event related averages for each ROI."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

NII_TC = "/Users/faruk/data/test-ERA/sub-08_task-amb_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF5c_sess-01_BBR_res2x_bvbabel.nii.gz"
NII_ROI = "/Users/faruk/data/test-ERA/sub-08_ROIs_in_VTC_shape.nii.gz"


# This affine gives starting indices at lower left hand corner in ITKSNAP
CUSTOM_AFFINE = np.array([[-1, 0, 0, 0],
		    			  [ 0, 1, 0, 0],
						  [ 0, 0, 1, 0],
				   		  [ 0, 0, 0, 1]])
# =============================================================================
# Step 1: Load nifti time course
nii1 = nb.load(NII_TC)
data1 = np.asarray(nii1.dataobj)
nr_timepoints = data1.shape[-1]
print(f"  Nr. timepoints {nr_timepoints}")

# Step 2: Load nifti roi
nii2 = nb.load(NII_ROI)
data2 = np.asarray(nii2.dataobj)
nr_voxels_of_interest = np.sum(data2 != 0)
print(f"  Nr. voxel of intrest {nr_voxels_of_interest}")

# Step 3: Determine labels of ROI's
labels = np.unique(data2)[1:]
nr_labels = labels.size
print(f"  Nr. labels {nr_labels}")

# Step 4: Determine voxels of interest
nr_voi = np.sum(data2 != 0)

# -----------------------------------------------------------------------------
# Step 5: Pull out time courses
voi_timecourses = np.zeros((nr_timepoints, nr_voi))
voi_timecourse_labels = np.zeros((nr_timepoints, nr_voi))
j = 0
k = 0
for i in labels:
	# Pull out ROI data
	mask = data2 == i
	k = np.sum(mask)
	temp = data1[mask].T

	# Sort by mean intensity
	temp_mean = np.mean(temp, axis=0)
	idx = np.argsort(temp_mean)
	temp2 = temp[:, idx]

	# Insert to carpet
	voi_timecourses[:, j:j+k] = temp2
	voi_timecourse_labels[:, j:j+k] = i
	j += k


# Save
basename = NII_TC.split(os.extsep, 1)[0]
outname = "{}_2D_VOI_TimeCourses.nii.gz".format(basename)
img = nb.Nifti1Image(voi_timecourses, affine=CUSTOM_AFFINE)
nb.save(img, outname)

outname = "{}_2D_VOI_TimeCourses_Labels.nii.gz".format(basename)
img = nb.Nifti1Image(voi_timecourse_labels, affine=CUSTOM_AFFINE)
nb.save(img, outname)

print("\nFinished.")
