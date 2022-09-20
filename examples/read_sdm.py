"""Read Brainvoyager sdm (single subject design matrix / motion estimates)."""

import bvbabel
import numpy as np

FILE = '/home/faruk/Git/bvbabel/test_data/sub-test04.sdm'

# =============================================================================

# Load design matrix
header, data = bvbabel.sdm.read_sdm(FILE)

# Print header information
print("\nSDM header")
for key, value in header.items():
    print("  ", key, ":", value)

print("\nSDM data")
txt = ""
for i in range(len(data)):
    txt += data[i]["NameOfPredictor"] + "  "
txt += '\n'

weights = np.zeros((header["NrOfDataPoints"], header["NrOfPredictors"]))
for i in range(len(data)):
    weights[:, i] = data[i]["ValuesOfPredictor"]

for i in range(header["NrOfDataPoints"]):
    for j in range(header["NrOfPredictors"]):
        txt += "{:>10.6f}".format(data[j]["ValuesOfPredictor"][i]) + "  "
    txt += '\n'

print(txt)

print("Finished.")
