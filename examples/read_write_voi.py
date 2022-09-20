"""Read and write BrainVoyager VOI (voxels of interest) file."""

import os
import bvbabel

FILE = "/home/faruk/Git/bvbabel/test_data/sub-test03.voi"

# =============================================================================
# Load VOI
header, data = bvbabel.voi.read_voi(FILE)

# Print header information
print("\nVOI header")
for key, value in header.items():
    print("  ", key, ":", value)

# Print data
print("\nVOI data")
for d in data:
    for key, value in d.items():
        print("  ", key, ":", value)

# Save VOI
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.voi".format(basename)
bvbabel.voi.write_voi(outname, header, data)

print("Finished.")
