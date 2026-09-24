"""Convert Freesurfer *.surf mesh to BrainVoyager SRF format"""

import os
import numpy as np
import nibabel.freesurfer as fs
import bvbabel
import timeit

# -----------------------------------------------------------------------------
# Input: FreeSurfer surface file
FILE = "rh.inflated"

# Read vertices and faces from .surf file
coords, faces = fs.read_geometry(FILE)
nr_verts = coords.shape[0]
nr_faces = faces.shape[0]

# -----------------------------------------------------------------------------
# Function to compute vertex normals
def compute_vertex_normals(verts, faces):
    def normalize_v3(arr):
        lens = np.linalg.norm(arr, axis=1)
        arr = arr / lens[:, np.newaxis]
        return arr

    norm = np.zeros_like(verts)
    tris = verts[faces]
    face_normals = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    face_normals = normalize_v3(face_normals)

    for i in range(3):
        norm[faces[:, i]] += face_normals

    return normalize_v3(norm)

# -----------------------------------------------------------------------------
# Transform coordinates to BrainVoyager's RAS convention
verts = np.stack((coords[:, 1], coords[:, 2], coords[:, 0]), axis=1)
verts[:, 1] *= -1  # Flip Y-axis

# Compute normals
norms = compute_vertex_normals(verts, faces)

# -----------------------------------------------------------------------------
# Find vertex neighbors
print("Finding vertex neighbors...")
start_time = timeit.default_timer()
nn = []
temp = faces.flatten()
for i in range(nr_verts):
    idx_faces = np.argwhere(temp == i) // 3
    temp_faces = np.squeeze(faces[idx_faces])
    nr_neighbors = temp_faces.shape[0]

    ord_edges = np.zeros((nr_neighbors, 3, 2), dtype=int)
    for j, t in enumerate(temp_faces):
        ord_edges[j, 0, :] = t[0:2]
        ord_edges[j, 1, :] = t[1:3]
        ord_edges[j, 2, :] = t[2], t[0]

    x = ord_edges != i
    x = x * x[:, :, ::-1]
    edges = ord_edges[x].reshape((nr_neighbors, 2))

    if len(edges) == 0:
        nn.append([0])  # fallback if no neighbors found
        continue

    idx_verts = [edges[0, 0], edges[0, 1]]
    edges_0 = edges[:, 0]
    edges_1 = edges[:, 1]
    n = 0
    while n < nr_neighbors - 2:
        matches = edges_1[edges_0 == idx_verts[-1]]
        if matches.size == 0:
            print(f"Warning: No further neighbor found for vertex {i} at step {n}")
            break
        next_vert = matches[0]
        idx_verts.append(next_vert)
        n += 1

    idx_verts.insert(0, len(idx_verts))  # number of neighbors first
    nn.append(idx_verts)
print("Done in", round(timeit.default_timer() - start_time, 2), "seconds.")

# -----------------------------------------------------------------------------
# Build SRF header
print("Writing SRF file...")
header = {
    "File version": 4,
    "Surface type": 2,
    "Nr vertices": nr_verts,
    "Nr triangles": nr_faces,
    "Mesh center X": np.mean(verts[:, 0]),
    "Mesh center Y": np.mean(verts[:, 1]),
    "Mesh center Z": np.mean(verts[:, 2]),
    "Vertex convex curvature R": 0.12,
    "Vertex convex curvature G": 0.39,
    "Vertex convex curvature B": 0.65,
    "Vertex convex curvature A": 1.0,
    "Vertex concave curvature R": 0.06,
    "Vertex concave curvature G": 0.20,
    "Vertex concave curvature B": 0.32,
    "Vertex concave curvature A": 1.0,
    "Nr triangle strip elements": 0,
    "MTC name": ''
}

# Prepare SRF data
mesh_data = {
    "vertices": verts,
    "vertex normals": norms,
    "faces": faces,
    "vertex colors": np.ones((nr_verts, 4)),  # RGBA = 4 channels per vertex
    "vertex neighbors": nn
}

# Create output filename
basename = os.path.basename(FILE).replace(".", "_")
outname = os.path.join(os.path.dirname(FILE), f"{basename}_bvbabel.srf")

# Write SRF file
bvbabel.srf.write_srf(outname, header, mesh_data)
print(f"✅ Finished writing: {outname}")