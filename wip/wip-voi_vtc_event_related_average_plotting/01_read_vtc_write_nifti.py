"""Read BrainVoyager VTC and export NIfTI."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

FILE = "/Users/faruk/data/test-ERA/sub-08_task-amb_acq-2depimb2_run-02_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF5c_sess-01_BBR_res2x.vtc"

# =============================================================================
# Load vtc
header, data = bvbabel.vtc.read_vtc(FILE, rearrange_data_axes=False)

# See header information
pprint(header)

# Transpose axes
data = np.transpose(data, [0, 2, 1, 3])
# Flip axes
data = data[::-1, ::-1, ::-1, :]

# Export nifti
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(data, affine=np.eye(4))
nb.save(img, outname)

print("Finished.")
