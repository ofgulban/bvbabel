"""Read Nifti write BrainVoyager VMR and V16 (anatomical image) files."""

import os
import bvbabel
import nibabel as nb
import numpy as np
import pprint
import shutil

FILE = "/Users/faruk/data/temp-David/SWI_0pt5_masked.nii.gz"
MASK = "/Users/faruk/data/temp-David/SWI_0pt5_mask-subdural_v06.nii.gz"
OUTDIR = "/Users/faruk/data/temp-David"

SUFFIX = "bvbabel"

PERC_MIN = 1
PERC_MAX = 99

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

# -----------------------------------------------------------------------------
# Load Nifti
nii = nb.load(FILE)
nii_data = np.nan_to_num(nii.get_fdata(), nan=0.)

# Load Mask
nii_mask = nb.load(MASK)
mask = np.asarray(nii_mask.dataobj, dtype=np.uint8)

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
# outname_v16 = "{}_{}.v16".format(basename, SUFFIX)
# bvbabel.v16.write_v16(outname_v16, v16_header, v16_data)

# -----------------------------------------------------------------------------
# Determine clip range
temp = nii_data[mask != 0]

thr_min, thr_max = np.percentile(temp, [PERC_MIN, PERC_MAX])

# Create VMR
vmr_header, vmr_data = bvbabel.vmr.create_vmr()

# Update VMR data (type cast nifti data to uint8 after range normalization)
vmr_data = np.copy(nii_data)
thr_min = int(thr_min / 100) * 100  # round
thr_max = int(thr_max / 100) * 100  # round
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
outname_vmr = "{}_{}_min-{}_max-{}.vmr".format(basename, SUFFIX, thr_min, thr_max)
bvbabel.vmr.write_vmr(outname_vmr, vmr_header, vmr_data)

print("---")
print(f"Min: {thr_min} | Max: {thr_max}")
print("---")

# =============================================================================
# Move generated files
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

# Copy to a new directory
shutil.copy(outname_vmr, OUTDIR)
# shutil.copy(outname_v16, OUTDIR)

# Remove old files
os.remove(outname_vmr)
# os.remove(outname_v16)

print("\nFinished.\n")
