"""Read and write BrainVoyager SDM (single subject design matrix)."""

import os
import bvbabel
import numpy as np
from pprint import pprint

FILE = '/home/faruk/Git/bvbabel/test_data/sub-test04.sdm'

# =============================================================================
# Load design matrix
header, data = bvbabel.sdm.read_sdm(FILE)

# Print header information
print("\nSDM header")
for key, value in header.items():
    print("  ", key, ":", value)

# Print data information
print("\nSDM data")
txt = ""
for i in range(len(data)):
    txt += data[i]["NameOfPredictor"] + "  "
txt += '\n'

for i in range(header["NrOfDataPoints"]):
    for j in range(header["NrOfPredictors"]):
        txt += "{:>10.6f}".format(data[j]["ValuesOfPredictor"][i]) + "  "
    txt += '\n'
print(txt)

# -----------------------------------------------------------------------------
# Put design matrix into a 2D numpy array
matrix = np.zeros((header["NrOfDataPoints"], header["NrOfPredictors"]))
for i in range(header["NrOfPredictors"]):
    for j in range(header["NrOfDataPoints"]):
        matrix[j, i] = data[i]["ValuesOfPredictor"][j]
print(matrix)
# -----------------------------------------------------------------------------

# Save SDM
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.sdm".format(basename)
bvbabel.sdm.write_sdm(outname, header, data)

print("Finished.")
