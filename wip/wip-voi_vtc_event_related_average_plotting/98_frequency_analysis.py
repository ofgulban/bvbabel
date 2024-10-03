"""Read NIFTI and plot event related averages for each ROI."""

import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt

NII_TC = "/Users/faruk/data/test-ERA/sub-08_task-amb_acq-2depimb2_run-01_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF5c_sess-01_BBR_res2x_bvbabel_2D_VOI_TimeCourses.nii.gz"

# =============================================================================
# Step 1: Load nifti time course
nii = nb.load(NII_TC)
data = nii.get_fdata()

# Step 2: Determine necessary information
nr_timepoints = data.shape[0]
nr_voxels = data.shape[1]
print(f"  Nr. timepoints {nr_timepoints}")
print(f"  Nr. voxels {nr_voxels}")

# -----------------------------------------------------------------------------
# TODO: What if we do frequency analysis?
# t = np.linspace(0, (nr_timepoints-1)*2, nr_timepoints)  # Time array from 0 to 1 with 1000 points

# for v in range(nr_voxels):
# 	fft_result = np.fft.fft(data[:, v])
# 	frequencies = np.fft.fftfreq(nr_timepoints, t[1] - t[0])

# # Plot the FFT result
# plt.figure(figsize=(10, 6))
# plt.plot(frequencies, np.abs(fft_result))
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Amplitude')
# plt.title('Frequency Spectrum')
# plt.grid(True)
# plt.show()

# print("Finished.")