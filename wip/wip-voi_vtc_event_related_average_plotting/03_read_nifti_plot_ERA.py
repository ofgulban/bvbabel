"""Read NIFTI and plot event related averages for each ROI."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

NII_TC = "/Users/faruk/data/test-ERA/sub-08_task-amb_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF5c_sess-01_BBR_res2x_bvbabel.nii.gz"
NII_ROI = "/Users/faruk/data/test-ERA/sub-08_ROIs_in_VTC_shape.nii.gz"

FILE_PRT = "/Users/faruk/data/test-ERA/Protocol_sub-08_Protocols_sess-01_Run01.prt"
TR_in_ms = 2000

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
voi_timecourses = np.zeros((nr_voi, nr_timepoints))
voi_timecourse_labels = np.zeros((nr_voi, nr_timepoints))
j = 0
k = 0
for i in labels:
	mask = data2 == i
	k = np.sum(mask)
	voi_timecourses[j:j+k, :] = data1[mask]
	voi_timecourse_labels[j:j+k, :] = i
	j += k

voi_timecourses = voi_timecourses.T
voi_timecourse_labels = voi_timecourse_labels.T

# -----------------------------------------------------------------------------
# TODO: Sort by brightness? within each ROI
# -----------------------------------------------------------------------------

# Save
basename = NII_TC.split(os.extsep, 1)[0]
outname = "{}_2D_VOI_TimeCourses.nii.gz".format(basename)
img = nb.Nifti1Image(voi_timecourses, affine=np.eye(4))
nb.save(img, outname)

outname = "{}_2D_VOI_TimeCourses_Labels.nii.gz".format(basename)
img = nb.Nifti1Image(voi_timecourse_labels, affine=np.eye(4))
nb.save(img, outname)

# -----------------------------------------------------------------------------
# Read PRT and put it into 2D nifti format
header_prt, data_prt = bvbabel.prt.read_prt(FILE_PRT)

# Print header information
print("\nPRT header")
for key, value in header_prt.items():
    print("  ", key, ":", value)

# Print data
print("\nPRT data")
for d in data_prt:
    for key, value in d.items():
        print("  ", key, ":", value)
    print("")

# Convert PRT to nifti
voi_timecourse_prt = np.zeros((nr_voi, nr_timepoints))
for i in range(int(header_prt["NrOfConditions"])):
	for ii in range(int(data_prt[i]["NrOfOccurances"])):
		j = round(float(data_prt[i]["Time start"][ii]) / TR_in_ms);
		k = round(float(data_prt[i]["Time stop"][ii]) / TR_in_ms);
		voi_timecourse_prt[:, j:k] = i

voi_timecourse_prt = voi_timecourse_prt.T

outname = "{}_2D_VOI_TimeCourses_PRT.nii.gz".format(basename)
img = nb.Nifti1Image(voi_timecourse_prt, affine=np.eye(4))
nb.save(img, outname)

print("\nFinished.")
