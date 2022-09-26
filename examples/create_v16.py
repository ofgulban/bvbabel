"""Create BrainVoyager v16 and save."""

import bvbabel

OUTNAME = "/Users/faruk/Documents/test_bvbabel/sub-test.v16"

# =============================================================================
header, data = bvbabel.v16.create_v16()
bvbabel.v16.write_v16(OUTNAME, header, data)

# Print header nicely
for key, value in header.items():
    print(key, ":", value)

print("Finished")
