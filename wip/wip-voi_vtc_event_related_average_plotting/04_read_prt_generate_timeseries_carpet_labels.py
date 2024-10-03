"""Read NIFTI and plot event related averages for each ROI."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

NII_TC = "/Users/faruk/data/test-ERA/sub-08_task-amb_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF5c_sess-01_BBR_res2x_bvbabel_2D_VOI_TimeCourses.nii.gz"

FILE_PRT = "/Users/faruk/data/test-ERA/Protocol_sub-08_Protocols_sess-01_Run01.prt"
TR_in_ms = 2000


# This affine gives starting indices at lower left hand corner in ITKSNAP
CUSTOM_AFFINE = np.array([[-1, 0, 0, 0],
		    			  [ 0, 1, 0, 0],
						  [ 0, 0, 1, 0],
				   		  [ 0, 0, 0, 1]])
# =============================================================================
# Step 1: Load nifti time course
nii1 = nb.load(NII_TC)
data1 = np.asarray(nii1.dataobj)

# Step 2: Determine necessary information
nr_timepoints = data1.shape[0]
nr_voxels = data1.shape[1]
print(f"  Nr. timepoints {nr_timepoints}")
print(f"  Nr. voxels {nr_voxels}")

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
voi_timecourse_prt = np.zeros((nr_voxels, nr_timepoints))
for i in range(int(header_prt["NrOfConditions"])):
	for ii in range(int(data_prt[i]["NrOfOccurances"])):
		j = round(float(data_prt[i]["Time start"][ii]) / TR_in_ms);
		k = round(float(data_prt[i]["Time stop"][ii]) / TR_in_ms);
		voi_timecourse_prt[:, j:k] = i

voi_timecourse_prt = voi_timecourse_prt.T

# Save
basename = NII_TC.split(os.extsep, 1)[0]
outname = "{}_PRT.nii.gz".format(basename)
img = nb.Nifti1Image(voi_timecourse_prt, affine=CUSTOM_AFFINE)
nb.save(img, outname)

print("\nFinished.")
