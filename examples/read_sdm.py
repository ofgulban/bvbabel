"""Read Brainvoyager sdm (single subject design matrix / motion estimates)."""

import bvbabel

FILE = '/home/faruk/Documents/test_bvbabel/sdm/faces_houses_design_matrix.sdm'

# =============================================================================

# Load design matrix
header, data = bvbabel.sdm.read_sdm(FILE)

# Print header information
print("\nSDM header")
for key, value in header.items():
    print("  ", key, ":", value)

print("\nSDM data")
txt = ''
for datapoint in range(header["NrOfDataPoints"]):
    for predno in range(header["NrOfPredictors"]):
        txt += ' ' + "{:>10.6f}".format(data[datapoint][predno])
    txt += '\n'
print(txt)

print("Finished.")
