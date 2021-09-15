"""Convert Nifti images with labels (integers only) to BrainVoyager VOI.

TODO:
    [ ] Read labels from csvs
    [ ] Read anatomical nifti to adjust voi headers

"""

import os
import csv
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt

NII_FILE = "/home/faruk/Downloads/neuroparc/atlases/label/Human/Yeo-7_space-MNI152NLin6_res-1x1x1.nii.gz"

COLORMAP = plt.cm.get_cmap('Spectral')

# =============================================================================
# Read nifti data
print("Reading nifti data...")
nii = nb.load(NII_FILE)
data = np.asarray(nii.dataobj)

# Adjust origin
data = np.transpose(data, [2, 1, 0])
data = data[::-1, :, :]

labels = np.unique(data)[1:]  # Do not include zeros
nr_voi = len(labels)

print("  Min: {} | Max : {}".format(data.min(), data.max()))
print("  Data type: {}".format(data.dtype))
print("  Nr. labels: {}".format(nr_voi))

print("Writing voi file...")
basename = NII_FILE.split(os.extsep, 1)[0]
voi_file = open(r"{}.voi".format(basename), "w")
voi_file.write("FileVersion: 4\n")
voi_file.write("\n")
voi_file.write("ReferenceSpace: BV\n")
voi_file.write("\n")
voi_file.write("OriginalVMRResolutionX: 1\n")
voi_file.write("OriginalVMRResolutionY: 1\n")
voi_file.write("OriginalVMRResolutionZ: 1\n")
voi_file.write("OriginalVMROffsetX: 0\n")
voi_file.write("OriginalVMROffsetY: 0\n")
voi_file.write("OriginalVMROffsetZ: 0\n")
voi_file.write("OriginalVMRFramingCubeDim: 256\n")
voi_file.write("\n")
voi_file.write("LeftRightConvention: 1\n")
voi_file.write("\n")
voi_file.write("SubjectVOINamingConvention: <VOI>_<SUBJ>\n")
voi_file.write("\n")
voi_file.write("\n")
voi_file.write("NrOfVOIs: {}\n".format(nr_voi))
voi_file.write("\n")

for n, i in enumerate(labels):
    label = "Label {}".format(str(i))
    color = COLORMAP((n / nr_voi) * 255)

    # Find voxel indices
    idx_voxels = np.argwhere(data == i)
    nr_voxels = idx_voxels.shape[0]

    voi_file.write("NameOfVOI: {}\n".format(label))
    voi_file.write("ColorOfVOI: {} {} {}\n".format(*color))
    voi_file.write("\n")
    voi_file.write("NrOfVoxels: {}\n".format(nr_voxels))

    for indices in idx_voxels:
        voi_file.write("{} {} {}\n".format(*indices))
    voi_file.write("\n")

voi_file.close()


print('Finished.')
