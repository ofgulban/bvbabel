"""Read BrainVoyager FMR file format."""

import csv
import numpy as np
import nibabel as nb

FILE = "/home/faruk/Documents/test_bvbabel/sub-01_ses-04_task-blocked_run-1_bold.fmr"
OUT_NII = "/home/faruk/Documents/test_bvbabel/sub-01_ses-04_task-blocked_run-1_bold_bvbabel.nii.gz"

# =============================================================================
info_fmr = dict()
info_pos = dict()
header_type = 0
with open(FILE, 'r') as f:

    # NOTE(Faruk): FMR files are complicated to parse because they can
    # contain multiple types of headers such as position information, slice
    # scan time table, and past transformations of the source nifti file.
    # I have decided to detect header type change based on double newline
    # characters.
    count_newline = 0
    while count_newline < 2:
        content = f.readline()
        content = content.strip()
        content = content.split(":")
        content = [i.strip() for i in content]

        if content[0] == "":
            count_newline += 1
            continue
        else:
            count_newline = 0

        if content[0] in ["Prefix", "LoadAMRFile", "ProtocolFile"]:
            info_fmr[content[0]] = content[1].strip("\"")
        else:
            info_fmr[content[0]] = content[1]

    # Expected fields are belong to position information
    count_newline = 0
    while count_newline < 2:
        content = f.readline()
        content = content.strip()
        content = content.split(":")
        content = [i.strip() for i in content]

        if content[0] == "":
            count_newline += 1
            continue
        else:
            count_newline = 0

        if content[0] == "PositionInformationFromImageHeaders":
            continue
        else:
            info_pos[content[0]] = content[1]


# Print header information
print("\nFMR information")
for key, value in info_fmr.items():
    print("  ", key, ":", value)

print("\nPosition information")
for key, value in info_pos.items():
    print("  ", key, ":", value)

# Test output data
# img_nii = nb.Nifti1Image(data, affine=np.eye(4))
# nb.save(img_nii, OUT_NII)
