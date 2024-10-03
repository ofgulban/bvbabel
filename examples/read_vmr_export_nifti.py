"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

FILE = "/Users/faruk/Documents/test-bvbabel/sub-test03.vmr"

# =============================================================================
# Load vmr
header, data = bvbabel.vmr.read_vmr(FILE)

# See header information
pprint.pprint(header)

# Prepare nifti
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.nii.gz".format(basename)
nii = nb.Nifti1Image(data, affine=np.eye(4))

# # (Optional) Insert vmr voxel dimensions
# nii.header["pixdim"][1] = header["VoxelSizeX"]
# nii.header["pixdim"][2] = header["VoxelSizeY"]
# nii.header["pixdim"][3] = header["VoxelSizeZ"]

# Save
nb.save(nii, outname)

print("Finished.")
