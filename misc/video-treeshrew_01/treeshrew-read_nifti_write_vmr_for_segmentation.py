"""Convert treeshrew segmentation nifti file to BrainVoyager format."""

import os
import bvbabel
import nibabel as nb
import numpy as np
import pprint

FILE = "/Users/faruk/data/temp-arcaro/video-2_tree_shrew/treeshrew-rim_v03.nii.gz"

SUFFIX = "bvbabel"

# =============================================================================
# Load Nifti
nii = nb.load(FILE)
nii_data = np.nan_to_num(nii.get_fdata(), nan=0.)

# (Optional) Adapt voxel labels to BrainVoyager
nii_data[nii_data == 3] = 100  # Gray matter
nii_data[nii_data == 2] = 150  # White matter
nii_data[nii_data == 1] = 0

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# (Optional - Use with caution!) Change the image orientation in BV
nii_data = np.transpose(nii_data, [2, 1, 0])

# (Optional - Use with caution!) Flip directions
nii_data = nii_data[::-1, :, :]
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

dims = nii_data.shape
voxdims = [nii.header["pixdim"][1],
           nii.header["pixdim"][2],
           nii.header["pixdim"][3]]

print("\n" + "="*79 + "\nNIFTI HEADER\n" + "="*79)
print(nii.header)

# -----------------------------------------------------------------------------
# Create VMR
vmr_header, vmr_data = bvbabel.vmr.create_vmr()

# Update VMR data (type cast nifti data to uint8 after range normalization)
vmr_data = np.copy(nii_data).astype(np.uint8)

# Update VMR headers
vmr_header["ColDirX"] = 0.0
vmr_header["ColDirY"] = 0.0
vmr_header["ColDirZ"] = 0.0
vmr_header["CoordinateSystem"] = 0
vmr_header["DimX"] = dims[1]  # nii.header["dim"][2]
vmr_header["DimY"] = dims[2]  # nii.header["dim"][3]
vmr_header["DimZ"] = dims[0]  # nii.header["dim"][1]
vmr_header["File version"] = 4
vmr_header["FoVCols"] = 0.0
vmr_header["FoVRows"] = 0.0
vmr_header["FramingCubeDim"] = np.max(nii_data.shape)
vmr_header["GapThickness"] = 0.0
vmr_header["LeftRightConvention"] = 1
vmr_header["NCols"] = 0
vmr_header["NRows"] = 0
vmr_header["NrOfPastSpatialTransformations"] = 0  # List here is for affine
vmr_header["OffsetX"] = 0
vmr_header["OffsetY"] = 0
vmr_header["OffsetZ"] = 0
vmr_header["PosInfosVerified"] = 1
vmr_header["ReferenceSpaceVMR"] = 0
vmr_header["RowDirX"] = 0.0
vmr_header["RowDirY"] = 0.0
vmr_header["RowDirZ"] = 0.0
vmr_header["Slice1CenterX"] = 0.0
vmr_header["Slice1CenterY"] = 0.0
vmr_header["Slice1CenterZ"] = 0.0
vmr_header["SliceNCenterX"] = 0.0
vmr_header["SliceNCenterY"] = 0.0
vmr_header["SliceNCenterZ"] = 0.0
vmr_header["SliceThickness"] = 0.0
vmr_header["VMROrigV16MaxValue"] = int(np.max(vmr_data))
vmr_header["VMROrigV16MeanValue"] = int(np.mean(vmr_data))
vmr_header["VMROrigV16MinValue"] = int(np.min(vmr_data))
vmr_header["VoxelResolutionInTALmm"] = 1
vmr_header["VoxelResolutionVerified"] = 1
vmr_header["VoxelSizeX"] = voxdims[0]
vmr_header["VoxelSizeY"] = voxdims[1]
vmr_header["VoxelSizeZ"] = voxdims[2]

print("\n" + "="*79 + "\nVMR HEADER\n" + "="*79)
pprint.pprint(vmr_header)

# Save VMR
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_{}.vmr".format(basename, SUFFIX)
bvbabel.vmr.write_vmr(outname, vmr_header, vmr_data)

print("\nFinished.\n")
