"""Read Nifti write BrainVoyager FMR file format."""

import os
import bvbabel
import nibabel as nb
import numpy as np

FILE = "/home/faruk/Documents/test_bvbabel/nifti_to_fmr/BOLD_interp.nii.gz"

# =============================================================================
# Load Nifti
nii = nb.load(FILE)
data = np.asarray(nii.dataobj)

# Create FMR

# Replace headers


# header, data = bvbabel.fmr.read_fmr(FILE)
#
# # Save FMR (and its paired STC file)
# basename = FILE.split(os.extsep, 1)[0]
# outname = "{}_bvbabel.fmr".format(basename)
# bvbabel.fmr.write_fmr(outname, header, data)

print("Finished.")
