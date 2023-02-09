"""Read and write BrainVoyager GLM (general linear model) file."""

import os
import bvbabel
from pprint import pprint

FILE = "/home/faruk/Documents/temp_bvbabel_glm/BOLD_whole_brain_3predictios.glm"

# =============================================================================
# Load vmr
header = bvbabel.glm.read_glm(FILE)

# See header information
pprint(header)

print("Finished.")
