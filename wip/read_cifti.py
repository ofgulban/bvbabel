"""Read CIFTI file import to Brainvoyager."""

import os
import nibabel as nb
import numpy as np
import bvbabel as bv

FILE = "/home/faruk/Documents/temp_CIFTI_conversion/Gordon333_FreesurferSubcortical.32k_fs_LR.dlabel.nii"

GII_NR_VERTICES_L = 32492  # Left hemisphere surface number of vertices
GII_NR_VERTICES_R = 32492  # Right hemisphere surface number of vertices

# =============================================================================
# Read Cifti
cifti = nb.load(FILE)
data = cifti.get_fdata().astype(int)
data = np.squeeze(data)

# Separate each hemispheres data
data_L = data[0:GII_NR_VERTICES_L]
data_R = data[GII_NR_VERTICES_L:GII_NR_VERTICES_L+GII_NR_VERTICES_R]

# Find unique labels
labels_L = np.unique(data_L)
labels_R = np.unique(data_R)

# Find number of labels
nr_pois_L = labels_L.size
nr_pois_R = labels_R.size

# Create an example POI
poi_header, poi_data = bv.poi.create_poi()

# -----------------------------------------------------------------------------
# Update POI header
poi_header["FromMeshFile"] = '"{}"'.format(FILE)
poi_header["NrOfMeshVertices"] = GII_NR_VERTICES_L
poi_header["NrOfPOIMTCs"] = 0
poi_header["NrOfPOIs"] = nr_pois_L

# -----------------------------------------------------------------------------
# Update POI data
poi_data = list()

idx = np.argwhere(data_L == 0)

idx.shape

for i, j in enumerate(labels_L):
    idx = np.argwhere(data_L == j) + 1
    poi_data.append(dict())
    poi_data[i]["NameOfPOI"] = '"{}"'.format(j)
    poi_data[i]["Vertices"] = idx[:, 0]
    poi_data[i]["ColorOfPOI"] = [255, 0, 0]
    poi_data[i]["LabelVertex"] = int(idx[0, 0])
    poi_data[i]["NrOfVertices"] = idx.size
    poi_data[i]["InfoTextFile"] = '""'


basename = FILE.split(os.extsep, 1)[0]
outname = "{}_L_bvbabel.poi".format(basename)
bv.poi.write_poi(outname, poi_header, poi_data)
