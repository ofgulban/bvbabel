"""Read BrainVoyager FMR file format and exxport it as Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel

FILE = "/Users/faruk/data/temp-kenshu/S05_ses1_run01_SCSA_3DMCTS_THPGLMF6c_ref.fmr"

# =============================================================================
# Load fmr
header, data = bvbabel.fmr.read_fmr(FILE)

# Save nifti for testing
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.nii.gz".format(basename)

# Export nifti (assign an identity matrix as affine with default header)
img = nb.Nifti1Image(data, affine=np.eye(4))

# Carry over equivalent header information
img.header["pixdim"][1] = header['InplaneResolutionX']
img.header["pixdim"][2] = header['InplaneResolutionY']
img.header["pixdim"][3] = header['SliceThickness']
img.header["pixdim"][4] = float(header['TR']) / 1000  # ms to s
img.affine[0, 0] *= img.header["pixdim"][1]
img.affine[1, 1] *= img.header["pixdim"][2]
img.affine[2, 2] *= img.header["pixdim"][3]

# Save
nb.save(img, outname)

print("Finished.")
