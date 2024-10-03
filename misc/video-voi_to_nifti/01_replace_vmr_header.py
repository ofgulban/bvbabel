"""Replace header of one VMR file with another."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint
from scipy.ndimage import zoom

FILE_VMR1 = "/Users/faruk/data/BV_SUPPORT/video/VTC_as_secondary_VMR.vmr"
FILE_VMR2 = "/Users/faruk/data/BV_SUPPORT/video/anatomical_MNI.vmr"

# =============================================================================
# Load
_, data_vmr = bvbabel.vmr.read_vmr(FILE_VMR1)
header_vmr, _ = bvbabel.vmr.read_vmr(FILE_VMR2)

# Write VMR
basename, extension = os.path.splitext(FILE_VMR1)
outname = "{}_bvbabel.vmr".format(basename)
bvbabel.vmr.write_vmr(outname, header_vmr, data_vmr)

print("Finished.")
