"""Read BrainVoyager FMR file format and exxport it as Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import itertools

FILE = "/Users/faruk/data/temp-kenshu/S06_RL_3DMCTS.fmr"

# =============================================================================
# Load fmr
header, data = bvbabel.fmr.read_fmr(FILE, rearrange_data_axes=True)

print(f" Read data dimensions: {data.shape}")


# Generate all permutations
axes = [0, 1, 2, 3]
permutations = list(itertools.permutations(axes))
for ax in permutations:
	data_rearranged = np.transpose(data, ax)
	print(f" New data dimensions : {ax} | {data_rearranged.shape}")

	# Save nifti for testing
	basename = FILE.split(os.extsep, 1)[0]
	outname = f"{basename}_bvbabel_ax-{ax[0]}{ax[1]}{ax[2]}{ax[3]}.nii.gz"

	# Generate Nifti
	img = nb.Nifti1Image(data_rearranged, affine=np.eye(4))

	# Save
	nb.save(img, outname)

print("Finished.")
