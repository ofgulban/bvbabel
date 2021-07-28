"""Read Brainvoyager smp file."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

FILE = "/home/faruk/Documents/test_bvbabel/srf_smp/maps.smp"

# =============================================================================
# Load vmr
header, data_smp = bvbabel.smp.read_smp(FILE)

# See header information
pprint(header)

# Save SMP
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.smp".format(basename)
bvbabel.smp.write_smp(outname, data_smp)

print("Finished.")
