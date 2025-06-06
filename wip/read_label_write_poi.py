import os
import numpy as np
import nibabel.freesurfer.io as fsio
import bvbabel
import pdb
# === Config ===
label_path = "file.label"
srf_path = "rh_white_bvbabel.srf"
poi_name = os.path.splitext(os.path.basename(label_path))[0]
color_rgb = (255, 0, 0)

# === Load label ===
vertices = fsio.read_label(label_path)

# === Load SRF ===
header_srf, _ = bvbabel.srf.read_srf(srf_path)
#db.set_trace()
n_mesh_vertices = header_srf["Nr vertices"]  # fixed lowercase key
mesh_name = os.path.basename(srf_path)



# === Build POI data ===
data_poi = [{
    "NameOfPOI": f'"{poi_name}"',  # ✅ enforce quotes
    "InfoTextFile": '""',
    "ColorOfPOI": np.array(color_rgb),
    "LabelVertex": int(vertices[0]),  # use first vertex as label
    "NrOfVertices": len(vertices),
    "Vertices": vertices.astype(np.int32),
    "VertexColorIndices": np.zeros(len(vertices), dtype=np.int32),
    "LabelVertex": int(vertices[0])  # ✅ first vertex in the list
}]

# === Build header ===
header_poi = {
    "FileVersion": 2,
    "FromMeshFile": f'"{os.path.basename(srf_path)}"',  # ✅ enforce quotes
    "NrOfMeshVertices": n_mesh_vertices,
    "NrOfPOIs": len(data_poi),
    "NrOfPOIMTCs": 0,
    "ReferenceSpace": 0,
    "OriginalVTCResolution": 0,
    "OriginalVTCXStart": 0,
    "OriginalVTCXEnd": 0,
    "OriginalVTCYStart": 0,
    "OriginalVTCYEnd": 0,
    "OriginalVTCZStart": 0,
    "OriginalVTCZEnd": 0
}

# === Save POI ===
poi_path = os.path.splitext(label_path)[0] + ".poi"
bvbabel.poi.write_poi(poi_path, header_poi, data_poi)
print(f"✅ POI saved to: {poi_path}")
