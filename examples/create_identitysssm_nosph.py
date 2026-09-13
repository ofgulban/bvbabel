"""
Create an identity SSM file for multi-run, single-subject analyses in
surface space without creating standard meshes via BrainVoyager's
Cortex-Based Alignment dialog.

The number of vertices is derived from the input SRF file.

"""

import bvbabel
import numpy as np

# Read surface information
srf_file = "/Users/BI/SampleData/GSG/sub-01_ses-04_T1w_IIHC_MNI_WM_RH_RECOSM.srf"
srf_header, _ = bvbabel.srf.read_srf(srf_file)
n_vertices = srf_header["Nr vertices"]

# Create an identity SSM matching the number of vertices in the surface
ssm_header, _ = bvbabel.ssm.create_ssm()
ssm_header['Nr vertices 1'] = n_vertices
ssm_header['Nr vertices 2'] = n_vertices
ssm_data = np.arange(n_vertices, dtype=np.int64)

# Save the SSM next to the input surface
ssm_file = srf_file[:-3]+'ssm'
bvbabel.ssm.write_ssm(ssm_file, ssm_header, ssm_data)

print(f"Identity SSM saved to: {ssm_file}")
