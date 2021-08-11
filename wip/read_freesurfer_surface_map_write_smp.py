"""Convert Freesurfer *.pct.mgh file into BrainVoyager SMP format."""

import os
import numpy as np
import nibabel as nb
import bvbabel

# NOTE: Full path to `<subjid>/surf/?h.w-g.pct.mgh` file. This file is a
# surface map that has gray to white matter signal intensity ratios for each
# vertex (ref: <https://surfer.nmr.mgh.harvard.edu/fswiki/pctsurfcon>)
FILE = "/home/faruk/Documents/temp_bvbabel_mgh/lh.w-g.pct.mgh"

# -----------------------------------------------------------------------------
# Read Freesurfer `*.w-g.pct.mgh` surface map
mgh = nb.load(FILE)
mgh_data = np.squeeze(np.asarray(mgh.dataobj))
nr_vertices = mgh_data.shape[0]

# Generate dummy SMP file
smp_header, smp_data = bvbabel.smp.generate_smp(nr_vertices=nr_vertices)

# Update some fields with mgh information
smp_header["Map"][0]["Threshold min"] = np.percentile(mgh_data, 5)
smp_header["Map"][0]["Threshold max"] = np.percentile(mgh_data, 95)

# Determine output name
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.smp".format(basename)

# Save SMP file while using the freesurfer MGH data
bvbabel.smp.write_smp(outname, smp_header, mgh_data[:, None])

print('Finished.')
