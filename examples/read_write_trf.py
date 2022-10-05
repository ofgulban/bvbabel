""" Examples reading and writing BrainVoyager transformation (TRF) file format."""

import os
import numpy as np
import bvbabel

# =============================================================================

filepath = '/Users/hester 1/Progprojs/Python/2022/for_bvbabel/bvbabel-main/test_data/sub-test06_trf/'
np.set_printoptions(suppress=True, formatter={'float_kind': '{:f}'.format})

filenames = ['fileversion8_IA.trf', 'fileversion8_FA.trf', 'fileversion8_transformationtype2_cMNI_a12.trf', 'fileversion8_aACPC.trf', 'fileversion8_ToMSP.trf',
             'fileversion8_transformationtype3_cMNI_a12_adjBBX.trf', 'fileversion7_extravmrtrf_IA.trf', 'fileversion7_extravmrtrf_FA.trf', 'fileversion5_IA.trf']
newnames = ['fileversion8_new_IA.trf', 'fileversion8_new_FA.trf', 'fileversion8_transformationtype2_new_cMNI_a12.trf', 'fileversion8_new_aACPC.trf', 'fileversion8_new_ToMSP.trf',
            'fileversion8_transformationtype3_new_cMNI_a12_adjBBX.trf', 'fileversion7_extravmrtrf_new_IA.trf', 'fileversion7_extravmrtrf_new_FA.trf', 'fileversion5_new_IA.trf']

for i, name in enumerate(filenames):
    filename = filepath + name
    header, data = bvbabel.trf.read_trf(filename)
    print('\nFilename: ' + filename)
    for key, value in header.items():
        print("  ", key, ":", value)
    for key, value in data.items():
        print("  ", key, ":", value)
    newname = filepath + newnames[i]
    bvbabel.trf.write_trf(newname, header, data)
