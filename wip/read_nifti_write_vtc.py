"""Read Nifti write BrainVoyager VTC file format."""

import os
import bvbabel
import nibabel as nb
import numpy as np

FILE = "/home/faruk/Documents/test_bvbabel/vtc2/sub-02_task-unamb_acq-3dvaso_run-avg_BOLD_interp_5vol.nii.gz"

# =============================================================================
# Load Nifti
nii = nb.load(FILE)
nii_data = np.asarray(nii.dataobj)
dims = nii_data.shape

# Create VTC
vtc_header, vtc_data = bvbabel.vtc.create_vtc()

# Update headers
vtc_header["Nr time points"] = dims[-1]
vtc_header["XStart"] = 0
vtc_header["XEnd"] = dims[1]
vtc_header["YStart"] = 0
vtc_header["YEnd"] = dims[2]
vtc_header["ZStart"] = 0
vtc_header["ZEnd"] = dims[0]

# Typecast when necessary and update the VTC header
vtc_data = nii_data.astype(np.float32)
vtc_header["Data type (1:short int, 2:float)"] = 2

# Mirror dimensions when necessary
vtc_data = vtc_data[::-1, :, :, :]

# Save VTC
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.vtc".format(basename)
bvbabel.vtc.write_vtc(outname, vtc_header, vtc_data)

print("Finished.")
