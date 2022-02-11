"""Convert Freesurfer *.gii triangular mesh surface to Wavefront .obj file."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import timeit

FILE = "/home/faruk/Documents/temp_bv_fsaverage/white_left.gii"

# -----------------------------------------------------------------------------
# Load data
gii = nb.load(FILE)
basename = FILE.split(os.extsep, 1)[0]


def compute_vertex_normals(verts, faces):
    """"Compute vertex normals.

    Parameters
    ----------
    verts: 2d numpy array, shape [nvertices, 3]
    Coordinates of vertices
    faces: 2d numpy array [nfaces, 3]
    Vertex indices forming triangles.

    Returns
    -------
    normals: 2d numpy array, shape [nvertices, 3]
    Unit vector vertex normals.

    Reference
    ---------
    https://sites.google.com/site/dlampetest/python/calculating-normals-of-a-triangle-mesh-using-numpy

    """
    def normalize_v3(arr):
        """Normalize a numpy array of 3 component vectors shape=(n, 3)."""
        lens = np.sqrt(arr[:, 0]**2. + arr[:, 1]**2. + arr[:, 2]**2.)
        arr[:, 0] /= lens
        arr[:, 1] /= lens
        arr[:, 2] /= lens
        return arr

    norm = np.zeros(verts.shape, dtype=verts.dtype)
    # Create an indexed view into the vertex array
    tris = verts[faces]
    # Calculate the normals (cross product of the vectors v1-v0 & v2-v0)
    n = np.cross(tris[::, 1] - tris[::, 0], tris[::, 2] - tris[::, 0])
    # Normalize weights in each normal equally.
    n = normalize_v3(n)
    # Convert face normals to vertex normals and normalize again
    norm[faces[:, 0]] += n
    norm[faces[:, 1]] += n
    norm[faces[:, 2]] += n
    return normalize_v3(norm)


# =============================================================================
# Extract vertices and faces
verts = gii.darrays[0].data
faces = gii.darrays[1].data
faces = faces[:, [0, 2, 1]]  # change winding (BV normals point inward)
norms = compute_vertex_normals(verts, faces)
nr_verts = verts.shape[0]
nr_faces = faces.shape[0]

# Manipulate coordinates to fit BrainVoyager's format
verts = np.stack((verts[:, 1], verts[:, 2], verts[:, 0]), axis=1)
verts[:, 1] *= -1
# faces = faces[:, [0, 2, 1]]  # change winding (BV normals point inward)
norms = compute_vertex_normals(verts, faces)

# center = 127.75;
# range = verts.max() - verts.min()
# mid = np.mean(verts, axis=0)
# verts[:, 0] = verts[:, 0] + center - mid[0];
# verts[:, 1] = verts[:, 1] + center - mid[1];
# verts[:, 2] = verts[:, 2] + center - mid[2];

# -----------------------------------------------------------------------------
# Compute_vertex_neighbours
# TODO: Convert this inta a function.
start_time = timeit.default_timer()
nn = []
temp = faces.flatten()  # This is done for speeding up argwhere
for i in range(nr_verts):  # loop over each vertex
    # Find faces that contain a given vertex id
    idx_faces = np.argwhere(temp == i)//3
    # Reduce to unique vertex ids
    idx_verts = np.unique(faces[idx_faces])
    # Remove the reference vertex id
    idx_verts = idx_verts[idx_verts != i]
    # Construct nearest neighbour array that starts with nr of neighbours
    nn_array = list(idx_verts)
    nn_array.insert(0, idx_verts.size)
    nn.append(nn_array)
elapsed = timeit.default_timer() - start_time
print(elapsed)

# -----------------------------------------------------------------------------
# Save SRF
print("Writing SRF file...")
header = dict()
header["File version"] = 4
header["Surface type"] = 2
header["Nr vertices"] = nr_verts
header["Nr triangles"] = nr_faces
header["Mesh center X"] = np.mean(verts[:, 0])
header["Mesh center Y"] = np.mean(verts[:, 1])
header["Mesh center Z"] = np.mean(verts[:, 2])
header["Vertex convex curvature R"] = 0.11999999731779099
header["Vertex convex curvature G"] = 0.38999998569488525
header["Vertex convex curvature B"] = 0.6499999761581421
header["Vertex convex curvature A"] = 1.0
header["Vertex concave curvature R"] = 0.05999999865889549
header["Vertex concave curvature G"] = 0.19499999284744263
header["Vertex concave curvature B"] = 0.32499998807907104
header["Vertex concave curvature A"] = 1.0
header["Nr triangle strip elements"] = 0
header["MTC name"] = ''

mesh_data = dict()
mesh_data["vertices"] = verts
mesh_data["vertex normals"] = norms
mesh_data["faces"] = faces
mesh_data["vertex colors"] = np.ones((verts.shape[0]))
mesh_data["vertex neighbors"] = nn

outname = "{}_bvbabel.srf".format(basename)
bvbabel.srf.write_srf(outname, header, mesh_data)

print("Finished.")
