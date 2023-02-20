"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

FILE = "/home/faruk/Documents/temp_bvbabel_glm/BOLD_whole_brain_GLM.glm"

# =============================================================================
# Load vmr
header, data = bvbabel.glm.read_glm(FILE)

# See header information
pprint.pprint(header)

# Export nifti
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(data, affine=np.eye(4))
nb.save(img, outname)

print("Finished.")
