"""Read BrainVoyager mgz converted vmr file to export mgz."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

# The original MGZ file before it is converted to BrainVoyager
MGZ_FILE = "/Users/faruk/Documents/temp-BVBABEL_VMR_TO_MGZ/T1.mgz"

# MGZ to VMR converted VMR file that we want to convert back to MGZ
VMR_FILE = "/Users/faruk/Documents/temp-BVBABEL_VMR_TO_MGZ/T1w_MPR_34_T1w_MPR_20260519112254_34_IIHC_ISO-1.vmr"

# =============================================================================
# Load mgz, needed for the affine information
mgz = nb.load(MGZ_FILE)

# Load vmr
header, data = bvbabel.vmr.read_vmr(VMR_FILE)

# See header information
pprint.pprint(header)

# Prepare nifti
basename = VMR_FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.mgz".format(basename)

# Transpose axes
data = np.transpose(data, [0, 2, 1])
# Flip axes
data = data[::-1, ::-1, :]

# Save
mgz = nb.MGHImage(data, affine=mgz.affine)
nb.save(mgz, outname)

print("Finished.")
