"""Read BrainVoyager srf & smp files to compute cortical magnification."""

import os
import numpy as np
from copy import copy
import bvbabel


FILE_SRF = "/home/faruk/Documents/test_bvbabel/SRF/surface.srf"
FILE_SMP = "/home/faruk/Documents/test_bvbabel/SRF/maps.smp"

# These values are required to compute vertex-wise distance in mm
VMR_IMAGE_DIMS = 512  # Stands for e.g. 512 x 512 x 512, or 256 x 256 x 256
VMR_VOXEL_DIMS = 0.4  # Stands for e.g 0.4 x 0.4 x 0.4 mm^3 ot 1 x 1 x 1 mm^3

# =============================================================================
# Load files
header_srf, data_srf = bvbabel.srf.read_srf(FILE_SRF)
header_smp, data_smp = bvbabel.smp.read_smp(FILE_SMP)

# Get vertex coordinates (2D numpy array)
vtx = data_srf["vertices"]
# Get vertex neighbors (python list)
nbr = data_srf["vertex neighbors"]
# Get PRF mapping visual field c & y coordinates
print(header_smp["Map"][1]["Name"])
print(header_smp["Map"][2]["Name"])
prf_xy = data_smp[:, 1:3]

# -----------------------------------------------------------------------------
print("Computing cortical magnification factors...")
# Prepare useful variables
nr_vtx = header_srf["Nr vertices"]
map_cmf = np.zeros(nr_vtx)

# Compute cortical magnification for each vertex
for v in range(nr_vtx):
    if prf_xy[v, 0] != 0 and prf_xy[v, 1] != 0:
        cmf_sum = 0
        n_count = 0
        for n in nbr[v][1:]:  # Loop over neighbor vertices
            # Compute vertex to vertex mesh distance
            dist_cortex = np.linalg.norm(vtx[v, :] - vtx[n, :])
            # Convert vertex to vertex mesh distance to millimeters
            dist_cortex *= (VMR_IMAGE_DIMS / 256) * VMR_VOXEL_DIMS

            # Compute vertex to vertex PRF xy coordinates distance
            dist_vfield = np.linalg.norm(prf_xy[v, :] - prf_xy[n, :])

            # Compute cortical magnification factor (CMF)
            # NOTE: CMF = "mm of cortical surface" / "degree of visual angle"
            if dist_vfield > 0:
                cmf_sum += dist_cortex / dist_vfield
                n_count += 1

        # Normalize cumulative CMF with the number of non-zero neighbours
        if cmf_sum > 0:
            cmf = cmf_sum / n_count

        # Put the vertex-wise average CMF into smp map format
        map_cmf[v] = cmf
    else:
        map_cmf[v] = 0

# -----------------------------------------------------------------------------
# Prepare new SMP map
header_smp["Nr maps"] += 1
header_smp["Map"].append(copy(header_smp["Map"][4]))
header_smp["Map"][-1]["Name"] = "CMF, UseThreshMap: R"
header_smp["Map"][-1]["Threshold min"] = 0.001
header_smp["Map"][-1]["Threshold max"] = 5.
header_smp["Map"][-1]["LUT file"] = "default_v21_inv.olt"
data_smp = np.hstack([data_smp, map_cmf[:, None]])

# Add reciprocal of CMF as it linearly increases with eccentricity
header_smp["Nr maps"] += 1
header_smp["Map"].append(copy(header_smp["Map"][4]))
header_smp["Map"][-1]["Name"] = "CMF reciprocal, UseThreshMap: R"
header_smp["Map"][-1]["Threshold min"] = 0.001
header_smp["Map"][-1]["Threshold max"] = 1.5
header_smp["Map"][-1]["LUT file"] = "default_v21_inv.olt"
map_cmf[map_cmf > 0] = 1 / map_cmf[map_cmf > 0]  # Reciprocal of non-zeros
data_smp = np.hstack([data_smp, map_cmf[:, None]])

# Save SMP
basename = FILE_SMP.split(os.extsep, 1)[0]
outname = "{}_bvbabel-CMF.smp".format(basename)
bvbabel.smp.write_smp(outname, header_smp, data_smp)

print("Finished.")
