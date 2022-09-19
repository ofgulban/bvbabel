"""Read Brainvoyager vmr, perform zero padding and write."""

import os
import bvbabel
import numpy as np

FILE = "/home/faruk/Documents/test_bvbabel/vtc2/anatomy_tmean.vmr"
PAD = 10  # x, y, z axes will be zero padded this many times

# =============================================================================
# Load vmr
header, data_img = bvbabel.vmr.read_vmr(FILE)

# Add dims
dims = data_img.shape
data_new = np.zeros([dims[0]+PAD, dims[1]+PAD, dims[2]+PAD],
                    dtype=data_img.dtype)
data_new[:dims[0], :dims[1], :dims[2]] = data_img

# Update header
header["DimX"] += PAD
header["DimY"] += PAD
header["DimZ"] += PAD
header["FramingCubeDim"] = max(dims) + PAD

# Write VMR
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_padded.vmr".format(basename)
bvbabel.vmr.write_vmr(outname, header, data_new)

print("Finished.")
