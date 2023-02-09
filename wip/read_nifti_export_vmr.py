"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

FILE = "/home/faruk/data2/DATA_BIGBRAIN/full16_100um_optbal_roi_500um.nii.gz"

# =============================================================================
# Create vmr
header, data = bvbabel.vmr.create_vmr()

# Load nifti
nii = nb.load(FILE)

# See header information
header_nii = [i for i in nii.header.items()]
pprint.pprint(header)

# Substitude header with nifti
header["DimX"] = nii.shape[0]
header["DimY"] = nii.shape[1]
header["DimZ"] = nii.shape[2]
header["FoVCols"] = nii.shape[0]
header["FoVRows"] = nii.shape[1]
header["FramingCubeDim"] = max(nii.shape)
header["NCols"] = nii.shape[0]
header["NRows"] = nii.shape[1]
header["VoxelResolutionInTALmm"] = 0
header["VoxelResolutionVerified"] = 0
header["VoxelSizeX"] = nii.header["pixdim"][0]
header["VoxelSizeY"] = nii.header["pixdim"][1]
header["VoxelSizeZ"] = nii.header["pixdim"][2]

# Substitude data with nifti
data = np.asarray(nii.dataobj, dtype=np.float32)
# Normalize to 0-225 range
thr_min, thr_max = np.percentile(data, [5, 95])
thr_range = thr_max - thr_min
data[data > thr_max] = thr_max
data -= thr_min
data[data < 0] = 0
data /= thr_range
data *= 225
data = data.astype(np.uint8)

data = np.transpose(data, (0, 2, 1))  # BV to Tal


# Export nifti
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.vmr".format(basename)
bvbabel.vmr.write_vmr(outname, header, data)

print("Finished.")
