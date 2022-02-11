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
faces = faces[:, [0, 2, 1]]
norms = compute_vertex_normals(verts, faces)
nr_verts = verts.shape[0]
nr_faces = faces.shape[0]

# -----------------------------------------------------------------------------
# Save OBJ
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.obj".format(basename)
print("Writing OBJ file...")
bvbabel.obj.write_obj(outname, verts, norms, faces)

print("Finished.")
