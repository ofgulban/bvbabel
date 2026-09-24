"""Convert Freesurfer curvature file into BrainVoyager SMP format."""

import os
import numpy as np
import nibabel.freesurfer as fs
import bvbabel

# -----------------------------------------------------------------------------
# Path to Freesurfer curvature file
FILE = "rh.curv"

# -----------------------------------------------------------------------------
# Load curvature data (1D array, per-vertex)
curv_data = fs.read_morph_data(FILE)

# Create SMP header/data
nr_vertices = curv_data.shape[0]
smp_header, smp_data = bvbabel.smp.create_smp(nr_vertices=nr_vertices)

# Update visualization thresholds
smp_header["Map"][0]["Threshold min"] = np.percentile(curv_data, 5)
smp_header["Map"][0]["Threshold max"] = np.percentile(curv_data, 95)

# Generate output path in the same directory
basename = os.path.basename(FILE).replace(".", "_")
output_dir = os.path.dirname(FILE)
outname = os.path.join(output_dir, f"{basename}_bvbabel.smp")

# Save SMP file
bvbabel.smp.write_smp(outname, smp_header, curv_data[:, None])

print(f"Finished writing: {outname}")
