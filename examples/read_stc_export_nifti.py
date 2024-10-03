"""Read BrainVoyager STC file format and export it as Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel

FILE = "/Users/faruk/data/temp-kenshu/S06_RL_3DMCTS.stc"

# =============================================================================
# Load stc (header of stc files are the fmr files)
data = bvbabel.stc.read_stc(
	FILE,
	nr_slices = 66,  # Enter this manually
	nr_volumes = 5,  # Enter this manually
	res_x = 224,     # Enter this manually
	res_y = 186,     # Enter this manually
	data_type=2,
	rearrange_data_axes=True
	)

# Save nifti for testing
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.nii.gz".format(basename)

# Generate Nifti
img = nb.Nifti1Image(data, affine=np.eye(4))

# Save
nb.save(img, outname)

print("Finished.")
