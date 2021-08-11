"""Convert mgz to nifti.

Dependencies
------------
- Freesurfer color look up table text file from:
<https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/AnatomicalROI/FreeSurferColorLUT>
- `aparc+aseg.mgz` file from Freesurfer.

"""

import os
import csv
import numpy as np
import nibabel as nb

NII_FILE = "/home/faruk/Documents/temp_bvbabel_mgh/aseg.mgz"
FREESURFER_LUT = "/home/faruk/Documents/temp_bvbabel_mgh/freesurfer_LUT.txt"

# =============================================================================
# Read freesurfer color look up table into dictionary
print("Reading freesurfer look up table...")
freesurfer_lut = {}
with open(FREESURFER_LUT) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if row:  # non-empty list
            temp = row[0].split()
            if temp[0][0] == "#":  # Comment
                pass
            else:
                freesurfer_lut.update({temp[0]: temp[1:]})

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

for i in labels:
    label = freesurfer_lut[str(i)][0]
    color = freesurfer_lut[str(i)][1:4]

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
