"""Read and write BrainVoyager GLM (general linear model) file."""

import os
import bvbabel
from pprint import pprint

FILE = "/home/faruk/Documents/temp_bvbabel_glm/BOLD_whole_brain_GLM.glm"

# =============================================================================
# Load vmr
header, data = bvbabel.glm.read_glm(FILE)

# See header information
pprint(header)

# TODO: Implement write GLM

print("Finished.")
