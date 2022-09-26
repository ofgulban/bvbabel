"""Read BrainVoyager gtc and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

FILE = "/home/faruk/Documents/test_bvbabel/gtc/gtc_test.gtc"

# =============================================================================
# Load file
header, data_img = bvbabel.gtc.read_gtc(FILE)

# See header information
pprint(header)

# Export nifti
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(data_img, affine=np.eye(4))
nb.save(img, outname)

print("Finished.")
