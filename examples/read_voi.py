"""Read Brainvoyager voi."""

import bvbabel

FILE = "/home/faruk/Documents/test_bvbabel/voi/sub-07_leftMT_Sphere16radius.voi"

# =============================================================================
# Load voi
header, data = bvbabel.voi.read_voi(FILE)

# Print header information
print("\nVOI header")
for key, value in header.items():
    print("  ", key, ":", value)

print("\nVOI data")
for d in data:
    for key, value in d.items():

        print("  ", key, ":", value)

print("Finished.")
