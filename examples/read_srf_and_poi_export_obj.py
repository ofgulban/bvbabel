"""Read BrainVoyager SRF and POI files to export Wavefront obj file."""

import os
import numpy as np
import bvbabel
from pprint import pprint

FILE_SRF = "/home/faruk/Documents/temp-bvbabel_SRF_POI/sub-01_WM_LH.srf"
FILE_POI = "/home/faruk/Documents/temp-bvbabel_SRF_POI/sub-01_WM_LH.poi"

# =============================================================================
# Load SRF
header_srf, data_srf = bvbabel.srf.read_srf(FILE_SRF)

# Load POI
header_poi, data_poi = bvbabel.poi.read_poi(FILE_POI)

# Create vertex colors based on the POI file
vertex_colors = np.ones((header_srf["Nr vertices"], 3))
for i in range(header_poi["NrOfPOIs"]):
    vertices = data_poi[i]["Vertices"]
    rgb = np.asarray(data_poi[i]["ColorOfPOI"]) / 255  # red green blue
    for j in vertices:
        vertex_colors[j, :] = rgb

# Save as colored OBJ file
print("Writing OBJ file...")
basename = FILE_SRF.split(os.extsep, 1)[0]
outname = "{}_bvbabel.obj".format(basename)
bvbabel.obj.write_obj_colored(outname,
                              data_srf["vertices"],
                              data_srf["vertex normals"],
                              data_srf["faces"],
                              vertex_colors)

print("Finished.")
