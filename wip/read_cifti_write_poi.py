"""Convert dlabel CIFTI file into Brainvoyager POI format."""

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
    # Iterate over volumetric and surface structures
    for name, data_indices, model in axis.iter_structures():
        # Look for a surface
        if name == surf_name:
            # Assume brainmodels axis is last, move it to front
            data = data.T[data_indices]
            # Generally 1-N, except medial wall vertices
            vtx_indices = model.vertex
            surf_data = np.zeros((vtx_indices.max() + 1,) + data.shape[1:],
                                 dtype=np.int32)
            surf_data[vtx_indices] = data
            return surf_data
    raise ValueError(f"No structure named {surf_name}")


def decompose_cifti(img):
    data = img.get_fdata(dtype=np.float32)
    brain_models = img.header.get_axis(1)  # Assume we know this
    return (surf_data_from_cifti(data, brain_models, "CIFTI_STRUCTURE_CORTEX_LEFT"),
            surf_data_from_cifti(data, brain_models, "CIFTI_STRUCTURE_CORTEX_RIGHT"))


data_L, data_R = decompose_cifti(cifti)

# -----------------------------------------------------------------------------
# Find unique labels
labels_L = np.unique(data_L).astype(np.int32)
labels_R = np.unique(data_R).astype(np.int32)

# Find number of labels
nr_pois_L = labels_L.size
nr_pois_R = labels_R.size

# =============================================================================
# Extract label name and color information
# =============================================================================
label_axis = cifti.header.get_axis(0)
label_dict = label_axis[0][1]

label_names = [label_dict[i][0] for i in range(len(label_dict))]
label_colors = list()
for i in range(len(label_dict)):
    RGBA = label_dict[i][1]
    RGBA = [int(RGBA[j]*255) for j in range(3)]
    label_colors.append(RGBA)

# -----------------------------------------------------------------------------
# Left hemisphere
# -----------------------------------------------------------------------------
# Create a placeholder POI
poi_header, poi_data = bv.poi.create_poi()

# Update POI header
poi_header["FromMeshFile"] = '"{}"'.format(FILE)
poi_header["NrOfMeshVertices"] = data_L.size
poi_header["NrOfPOIMTCs"] = 0
poi_header["NrOfPOIs"] = nr_pois_L

# Update POI data
poi_data = list()
idx = np.argwhere(data_L == 0)
for i, j in enumerate(labels_L):
    idx = np.where(data_L == j)[0]
    poi_data.append(dict())
    poi_data[i]["NameOfPOI"] = '"{}"'.format(label_names[j])
    poi_data[i]["Vertices"] = idx
    poi_data[i]["ColorOfPOI"] = [label_colors[j][0], label_colors[j][1], label_colors[j][2]]
    poi_data[i]["LabelVertex"] = int(idx[0])
    poi_data[i]["NrOfVertices"] = idx.size
    poi_data[i]["InfoTextFile"] = '""'

# Save
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_L_bvbabel.poi".format(basename)
bv.poi.write_poi(outname, poi_header, poi_data)

# -----------------------------------------------------------------------------
# Right hemisphere
# -----------------------------------------------------------------------------
# Create a placeholder POI
poi_header, poi_data = bv.poi.create_poi()

# Update POI header
poi_header["FromMeshFile"] = '"{}"'.format(FILE)
poi_header["NrOfMeshVertices"] = data_R.size
poi_header["NrOfPOIMTCs"] = 0
poi_header["NrOfPOIs"] = nr_pois_L

# Update POI data
poi_data = list()
idx = np.argwhere(data_R == 0)
for i, j in enumerate(labels_R):
    idx = np.where(data_R == j)[0]
    poi_data.append(dict())
    poi_data[i]["NameOfPOI"] = '"{}"'.format(label_names[j])
    poi_data[i]["Vertices"] = idx
    poi_data[i]["ColorOfPOI"] = [label_colors[j][0], label_colors[j][1], label_colors[j][2]]
    poi_data[i]["LabelVertex"] = int(idx[0])
    poi_data[i]["NrOfVertices"] = idx.size
    poi_data[i]["InfoTextFile"] = '""'

# Save
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_R_bvbabel.poi".format(basename)
bv.poi.write_poi(outname, poi_header, poi_data)


print("Finished.")
