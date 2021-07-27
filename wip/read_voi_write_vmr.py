"""Read Brainvoyager voi."""

import os
import bvbabel
import numpy as np

FILE = "/home/faruk/Documents/test_bvbabel/voi/aparc+aseg.voi"

# =============================================================================
# Load voi
voi_header, voi_data = bvbabel.voi.read_voi(FILE)

# Print header information
print("\nVOI header")
for key, value in voi_header.items():
    print("  ", key, ":", value)

dims = np.repeat(voi_header["OriginalVMRFramingCubeDim"], 3)
temp = np.zeros(dims)

for i in range(len(voi_data)):
    idx = voi_data[i]["Coordinates"]
    x = idx[:, 0] + voi_header["OriginalVMROffsetX"]
    y = idx[:, 1] + voi_header["OriginalVMROffsetY"]
    z = idx[:, 2] + voi_header["OriginalVMROffsetZ"]
    temp[x, y, z] = i + 1  # +1 to skip zero

# -----------------------------------------------------------------------------
# TODO: Implement generate VMR
vmr_header, vmr_data = bvbabel.vmr.generate_vmr()

# Write VMR
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.vmr".format(basename)
bvbabel.vmr.write_vmr(outname, vmr_header, vmr_data)

print("Finished.")
