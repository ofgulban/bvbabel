"""Read Nifti write BrainVoyager VMR and V16 (anatomical image) files."""
import os
import bvbabel
import nibabel as nb
import numpy as np
import pprint

FILE = "/home/faruk/data2/DATA-AHEAD/temp/Ahead_brain_122017_blockface-image_ISO.nii.gz"

SUFFIX = "bvbabel"

# =============================================================================
# Load Nifti
nii = nb.load(FILE)
nii_data = np.nan_to_num(nii.get_fdata(), nan=0.)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# # (Optional - Use with caution!) Change the image orientation in BV
# change orientation, if required to RAS+
# input_orient = nb.aff2axcodes(nii.affine)
# output_orient = (('L','R'),('P','A'),('I','S')) # RAS+
# ornt = nb.orientations.axcodes2ornt(input_orient, output_orient)
# nii_data = nb.orientations.apply_orientation(nii_data, ornt)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

dims = nii_data.shape
voxdims = [nii.header["pixdim"][1],
           nii.header["pixdim"][2],
           nii.header["pixdim"][3]]

print("\n" + "="*79 + "\nNIFTI HEADER\n" + "="*79)
print(nii.header)

# -----------------------------------------------------------------------------
# Create V16
v16_header, v16_data = bvbabel.v16.create_v16()

# Create V16 data (type cast nifti data to uint16 after range normalization)
v16_data = np.copy(nii_data)
thr_min, thr_max = np.percentile(v16_data[v16_data != 0], [0, 100])
v16_data[v16_data > thr_max] = thr_max
v16_data[v16_data < thr_min] = thr_min
v16_data = v16_data - thr_min
v16_data = v16_data / (thr_max - thr_min) * 65535
v16_data = np.asarray(v16_data, dtype=np.ushort)

# Update V16 headers
v16_header["DimX"] = dims[1]  # nii.header["dim"][2]
v16_header["DimY"] = dims[2]  # nii.header["dim"][3]
v16_header["DimZ"] = dims[0]  # nii.header["dim"][1]

print("\n" + "="*79 + "\nV16 HEADER\n" + "="*79)
pprint.pprint(v16_header)

# Save V16
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_{}.v16".format(basename, SUFFIX)
bvbabel.v16.write_v16(outname, v16_header, v16_data)

# -----------------------------------------------------------------------------
# Create VMR
vmr_header, vmr_data = bvbabel.vmr.create_vmr()

# Update VMR data (type cast nifti data to uint8 after range normalization)
vmr_data = np.copy(nii_data)
thr_min, thr_max = np.percentile(vmr_data[vmr_data != 0], [1, 99])
vmr_data[vmr_data > thr_max] = thr_max
vmr_data[vmr_data < thr_min] = thr_min
vmr_data = vmr_data - thr_min
vmr_data = vmr_data / (thr_max - thr_min) * 225  # Special BV range
vmr_data = np.asarray(vmr_data, dtype=np.ubyte)

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
vmr_header["VMROrigV16MaxValue"] = int(np.max(v16_data))
vmr_header["VMROrigV16MeanValue"] = int(np.mean(v16_data))
vmr_header["VMROrigV16MinValue"] = int(np.min(v16_data))
vmr_header["VoxelResolutionInTALmm"] = 1
vmr_header["VoxelResolutionVerified"] = 1
vmr_header["VoxelSizeX"] = voxdims[0]
vmr_header["VoxelSizeY"] = voxdims[1]
vmr_header["VoxelSizeZ"] = voxdims[2]

print("\n" + "="*79 + "\nVMR HEADER\n" + "="*79)
pprint.pprint(vmr_header)

# Save VMR
outname = "{}_{}.vmr".format(basename, SUFFIX)
bvbabel.vmr.write_vmr(outname, vmr_header, vmr_data)

print("\nFinished.\n")
