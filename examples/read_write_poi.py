"""Read and write BrainVoyager POI (surface patches of interest) file."""

import os
import bvbabel

FILE = "/home/faruk/Documents/test_bvbabel/poi/sub-test03_cube.poi"

# =============================================================================
# Load VOI
header, data = bvbabel.poi.read_poi(FILE)

# Print header information
print("\nPOI header")
for key, value in header.items():
    print("  ", key, ":", value)

# Print data
print("\nPOI data")
for d in data:
    for key, value in d.items():
        print("  ", key, ":", value)
    print("")

# Save POI
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.poi".format(basename)
bvbabel.poi.write_poi(outname, header, data)

print("Finished.")
