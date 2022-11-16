"""Read CIFTI file import to Brainvoyager."""

import os
import nibabel as nb
import numpy as np
import bvbabel as bv

FILE = "/home/faruk/Documents/temp_CIFTI_conversion/null_lL_WG33/Gordon333_FreesurferSubcortical.32k_fs_LR.dlabel.nii"

# =============================================================================
# Read Cifti
cifti = nb.cifti2.load(FILE)

# -----------------------------------------------------------------------------
# NOTE: Taken from: https://nbviewer.org/github/neurohackademy/nh2020-curriculum/blob/master/we-nibabel-markiewicz/NiBabel.ipynb
def surf_data_from_cifti(data, axis, surf_name):
    assert isinstance(axis, nb.cifti2.BrainModelAxis)
    for name, data_indices, model in axis.iter_structures():  # Iterates over volumetric and surface structures
        if name == surf_name:                                 # Just looking for a surface
            data = data.T[data_indices]                       # Assume brainmodels axis is last, move it to front
            vtx_indices = model.vertex                        # Generally 1-N, except medial wall vertices
            surf_data = np.zeros((vtx_indices.max() + 1,) + data.shape[1:], dtype=data.dtype)
            surf_data[vtx_indices] = data
            return surf_data
    raise ValueError(f"No structure named {surf_name}")


def decompose_cifti(img):
    data = img.get_fdata(dtype=np.float32)
    brain_models = img.header.get_axis(1)  # Assume we know this
    return (surf_data_from_cifti(data, brain_models, "CIFTI_STRUCTURE_CORTEX_LEFT"),
            surf_data_from_cifti(data, brain_models, "CIFTI_STRUCTURE_CORTEX_RIGHT"))


data_L, data_R = decompose_cifti(cifti)
print(left.shape, right.shape)
# -----------------------------------------------------------------------------

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
for i, j in enumerate(labels_L):
    idx = np.where(data_L == j)[0]
    poi_data.append(dict())
    poi_data[i]["NameOfPOI"] = '"{}"'.format(int(j))
    poi_data[i]["Vertices"] = idx
    poi_data[i]["ColorOfPOI"] = [255, 0, 0]
    poi_data[i]["LabelVertex"] = int(idx[0])
    poi_data[i]["NrOfVertices"] = idx.size
    poi_data[i]["InfoTextFile"] = '""'

basename = FILE.split(os.extsep, 1)[0]
outname = "{}_L_bvbabel.poi".format(basename)
bv.poi.write_poi(outname, poi_header, poi_data)

print("Finished.")
