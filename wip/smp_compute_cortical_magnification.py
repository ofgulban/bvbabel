"""Read Brainvoyager srf & smp files to compute cortical magnification."""

import os
import numpy as np
from copy import copy
import bvbabel


FILE_SRF = "/home/faruk/Documents/test_bvbabel/srf_smp/surface.srf"
FILE_SMP = "/home/faruk/Documents/test_bvbabel/srf_smp/maps.smp"

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
# Get eccentricity & polar angle
print(header_smp["Map"][4]["Name"])
map_polar = data_smp[:, 4]
map_eccen = data_smp[:, 5]

# -----------------------------------------------------------------------------
# Prepare useful variables
nr_vtx = header_srf["Nr vertices"]
map_new = np.zeros(nr_vtx)

# Convert eccentricity and polar angle to carthesian coordinates
cart = np.zeros([nr_vtx, 2])
cart[:, 0] = map_eccen * np.cos(map_polar)
cart[:, 1] = map_eccen * np.sin(map_polar)

# Compute cortical magnification for each vertex
for v in range(nr_vtx):
    if map[v] != 0:
        # ---------------------------------------------------------------------
        # Compute distance in space between neighboring vertices
        dist_sum = 0
        for n in nbr[v][1:]:  # Loop over neighbor vertices
            dist = np.linalg.norm(vtx[v, :] - vtx[n, :])  # Euclidean distance
            dist_sum += dist  # Add distance between each neighbor vertex
        dist_avg_space = dist_sum / nbr[v][0]  # Normalize with nr of neighbors

        # Standardize with voxel size and mesh to vmr scale. When properly set
        # this scaling converts vertex-wise distance measurement units to
        # millimeters.
        dist_avg_space *= (VMR_IMAGE_DIMS / 256) * VMR_VOXEL_DIMS

        # ---------------------------------------------------------------------
        # Compute distance in visual field between neighboring vertices
        dist_sum = 0
        for n in nbr[v][1:]:
            dist = np.linalg.norm(cart[v, :] - cart[n, :])
            dist_sum += dist
        dist_avg_visfield = dist_sum / nbr[v][0]

        # ---------------------------------------------------------------------
        # Compute cortical magnification factor (CMF)
        cmf = dist_avg_space / dist_avg_visfield
        map_new[v] = cmf
    else:
        map_new[v] = 0

# -----------------------------------------------------------------------------
# Prepare new SMP map
header_smp["Nr maps"] += 1
header_smp["Map"].append(copy(header_smp["Map"][4]))
header_smp["Map"][6]["Name"] = "Cortical Magnification Factor, UseThreshMap: R"
header_smp["Map"][6]["Threshold min"] = 0.001
header_smp["Map"][6]["Threshold max"] = 10.
header_smp["Map"][6]["LUT file"] = "default_v21_inv.olt"

data_smp = np.hstack([data_smp, map_new[:, None]])

# Save SMP
basename = FILE_SMP.split(os.extsep, 1)[0]
outname = "{}_bvbabel-CMF.smp".format(basename)
bvbabel.smp.write_smp(outname, header_smp, data_smp)

print("Finished.")
