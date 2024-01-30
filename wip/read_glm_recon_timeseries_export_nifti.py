"""!!!WIP!!! Read BrainVoyager GLM and export reconstructed timeseries."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

FILE_GLM = "/Users/faruk/data/temp-GLM/test2.glm"

# =============================================================================
# Load
header_glm, _, _, data_beta, _, data_meantc, _ = bvbabel.glm.read_glm(FILE_GLM)

# -----------------------------------------------------------------------------
# Reconstruct timeseries
preds = header_glm["Design matrix"]
recon = np.zeros(data_meantc.shape + (header_glm["Nr time points"],))
for i in range(header_glm["Nr all predictors"]):
	# Multiply predictor with beta
	recon += preds[:, i] * data_beta[:, :, :, i, None]

# # Add intercept if constant term is not a predictor
# if data_sdm[i]["NameOfPredictor"] != "Constant":
# 	recon += data_meantc[:, :, :, None]

# -----------------------------------------------------------------------------
# Export nifti
basename = FILE_GLM.split(os.extsep, 1)[0]

# Reconstructed values
outname = "{}_recon_bvbabel.nii.gz".format(basename)
img = nb.Nifti1Image(recon[:, :, :, 0:100], affine=np.eye(4))
nb.save(img, outname)

print("Finished.")
