"""Convert BrainVoyager VOI files into VTC sized Nifti files."""

import os
import bvbabel
import numpy as np
import nibabel as nb
from pprint import pprint


FILE_VOI = "/Users/faruk/data/test-ERA/sub-08_ROIs.voi"
FILE_VTC = "/Users/faruk/data/test-ERA/sub-08_task-amb_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF5c_sess-01_BBR_res2x.vtc"
FILE_VMR = "/Users/faruk/data/test-ERA/sub-08_sess-01_acq-mp2rage_UNI_denoised_IIHC_bvbabel_SSbet_BFC_res2x.vmr"

# =============================================================================
# Step 1: Load voi
header_voi, data_voi = bvbabel.voi.read_voi(FILE_VOI)

# Print header information
print("\nVOI header")
for key, value in header_voi.items():
    print("  ", key, ":", value)

# -----------------------------------------------------------------------------
# Step 2: Get necessary information from VTC header
header_vtc, data_vtc = bvbabel.vtc.read_vtc(FILE_VTC, rearrange_data_axes=False)

# See header information
print("\nVTC header")
pprint(header_vtc)

# Necessary header information
vtc_scale   = header_vtc["VTC resolution relative to VMR (1, 2, or 3)"]

# -----------------------------------------------------------------------------
# Step 3: Get necessary information from VMR header
header_vmr, data_vmr = bvbabel.vmr.read_vmr(FILE_VMR)

# Print header nicely
print("\nVMR header")
for key, value in header_vmr.items():
    print(key, ":", value)

# Necessary header information
vmr_DimX = header_vmr["DimX"]
vmr_DimY = header_vmr["DimY"]
vmr_DimZ = header_vmr["DimZ"]

# -----------------------------------------------------------------------------
# Step 4: Generate a VTC sized nifti
temp = np.zeros(data_vtc.shape[:-1])

# Transpose axes
temp = np.transpose(temp, [0, 2, 1])

# -----------------------------------------------------------------------------
# Step 5: Insert VOI into VTC sized Nifti
for i in range(len(data_voi)):
    idx = data_voi[i]["Coordinates"]
    x = (idx[:, 0] - header_vtc['XStart']) // vtc_scale
    y = (idx[:, 1] - header_vtc['YStart']) // vtc_scale
    z = (idx[:, 2] - header_vtc['ZStart']) // vtc_scale
    temp[z, x, y] = i + 1  # +1 to skip zero

# Flip axes
temp = temp[::-1, ::-1, ::-1]

# -----------------------------------------------------------------------------
# Step 6: Export nifti
basename = FILE_VOI.split(os.extsep, 1)[0]
outname = "{}_in_VTC_shape.nii.gz".format(basename)
img = nb.Nifti1Image(temp, affine=np.eye(4))
nb.save(img, outname)

print("\nFinished.")

