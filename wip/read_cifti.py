"""Read CIFTI file import to Brainvoyager."""

import nibabel as nb
import numpy as np

FILE = "/home/faruk/Documents/temp_CIFTI_conversion/Gordon333_FreesurferSubcortical.32k_fs_LR.dlabel.nii"

# =============================================================================
cifti = nb.load(FILE)

data = cifti.get_fdata()
