"""Read BrainVoyager FMR file format."""

import os
import numpy as np
import nibabel as nb
import bvbabel

FILE = "/home/faruk/Documents/test_bvbabel/fmr/nifti_converted.fmr"

# =============================================================================
# Load fmr
header, data = bvbabel.fmr.read_fmr(FILE)

# Save nifti for testing
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.nii.gz".format(basename)

# Export nifti (assign an identity matrix as affine with default header)
img = nb.Nifti1Image(data, affine=np.eye(4))
nb.save(img, outname)

# -----------------------------------------------------------------------------
# NOTE[Faruk]: I need to think about exporting nifti with a header that matches
# the fmr header fields

# Export nifti (Pull affine matrix from fmr header)
# affine = header["Transformation information"]["Transformation matrix"]
# img = nb.Nifti1Image(data, affine=affine)
# nb.save(img, outname)
# -----------------------------------------------------------------------------

print("Finished.")
