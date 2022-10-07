"""Read and write BrainVoyager PRT (protocol) file."""

import os
import bvbabel

FILE = "/home/faruk/Git/bvbabel/test_data/sub-test05.prt"

# =============================================================================
# Load VOI
header, data = bvbabel.prt.read_prt(FILE)

# Print header information
print("\nPRT header")
for key, value in header.items():
    print("  ", key, ":", value)

# Print data
print("\nPRT data")
for d in data:
    for key, value in d.items():
        print("  ", key, ":", value)
    print("")

# Save PRT
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.prt".format(basename)
bvbabel.prt.write_prt(outname, header, data)

print("Finished.")
