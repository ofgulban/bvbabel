"""Read and write BrainVoyager transformation (TRF) files."""

import os
import numpy as np
import bvbabel

FILEDIR = '/home/faruk/Git/bvbabel/test_data/trf/'

FILENAMES = [
    "sub-test06_fileversion-5_IA.trf",
    "sub-test06_fileversion-7_extravmrtrf_FA.trf",
    "sub-test06_fileversion-7_extravmrtrf_IA.trf",
    "sub-test06_fileversion-8_aACPC.trf",
    "sub-test06_fileversion-8_FA.trf",
    "sub-test06_fileversion-8_IA.trf",
    "sub-test06_fileversion-8_ToMSP.trf",
    "sub-test06_fileversion-8_transformationtype2_cMNI_a12.trf",
    "sub-test06_fileversion-8_transformationtype3_cMNI_a12_adjBBX.trf"
    ]

# =============================================================================
np.set_printoptions(suppress=True, formatter={'float_kind': '{:f}'.format})
for f in FILENAMES:
    file = os.path.join(FILEDIR, f)
    header, data = bvbabel.trf.read_trf(file)

    print('\nFilename: {}'.format(f))
    for key, value in header.items():
        print("  ", key, ":", value)
    for key, value in data.items():
        print("  ", key, ":", value)

    basename = file.split(os.extsep, 1)[0]
    outname = "{}_bvbabel.trf".format(basename)
    bvbabel.trf.write_trf(outname, header, data)
