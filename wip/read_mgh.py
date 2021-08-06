"""Convert mgz to nifti."""

import os
import numpy as np
from nibabel import load, save, Nifti1Image

FILE = "/home/faruk/Documents/test_bvbabel/MGH/lh.w-g.pct.mgh"

mgz = load(FILE)
data = np.asarray(mgz.dataobj)

print(data.shape)

print('Finished.')
