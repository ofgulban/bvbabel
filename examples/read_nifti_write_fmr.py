"""Read Nifti write BrainVoyager FMR (functional MR timeseries) files."""
import os
import bvbabel
import nibabel as nb
import numpy as np
import pprint

FILE = "/Users/faruk/data/temp-logan_phase_jolt/fine/sub-3003_ses-fine_task-fncloc_run-1_part-mag_bold.nii.gz"

SUFFIX = "bvbabel"

# =============================================================================
# Load Nifti
nii = nb.load(FILE)
nii_data = np.asarray(nii.dataobj, dtype=np.uint16)

# -----------------------------------------------------------------------------
# Extract nifti header information
dims = nii_data.shape
voxdims = [nii.header["pixdim"][1],
           nii.header["pixdim"][2],
           nii.header["pixdim"][3]]
TR = nii.header["pixdim"][4] * 1000 # ms

print("\n" + "="*79 + "\nNIFTI HEADER\n" + "="*79)
print(nii.header)

# -----------------------------------------------------------------------------
# Create FMR
fmr_header, _ = bvbabel.fmr.create_fmr()

# Update headers
fmr_header["NrOfVolumes"] = dims[3]
fmr_header["NrOfSlices"] = dims[2]
fmr_header["NrOfSkippedVolumes"] = 0
fmr_header["Prefix"] = "bvbabel"
fmr_header["DataType"] = 1  # 1: 2-byte int; 2:4-byte float 
fmr_header["TR"] = TR
fmr_header["InterSliceTime"] = 1  # << Not written in some niftis
fmr_header["TimeResolutionVerified"] = 1
fmr_header["TE"] = 10  # << Not written in some niftis
fmr_header["SliceAcquisitionOrder"] = 5  # << Not written in some niftis
fmr_header["ResolutionX"] = dims[0]
fmr_header["ResolutionY"] = dims[1]
fmr_header["ImageIndex"] = 0
fmr_header["LayoutNColumns"] = int(np.floor(np.sqrt(fmr_header["NrOfSlices"])))
fmr_header["LayoutNRows"] = int(np.ceil(np.sqrt(fmr_header["NrOfSlices"])))
fmr_header["InplaneResolutionX"] = voxdims[0]
fmr_header["InplaneResolutionY"] = voxdims[1]
fmr_header["SliceThickness"] = voxdims[2]
fmr_header["SliceGap"] = 0

print("\n" + "="*79 + "\nFMR HEADER\n" + "="*79)
pprint.pprint(fmr_header)

# Save
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_{}.fmr".format(basename, SUFFIX)
bvbabel.fmr.write_fmr(outname, fmr_header, nii_data)

print("\nFinished.\n")
