"""Convert Freesurfer *.gii triangular mesh surface to Wavefront .obj file."""

import os
import numpy as np
import nibabel as nb
import bvbabel

FILE = "/home/faruk/gdrive/bvbabel/fsaverage/fsaverage/white_left.gii"

# -----------------------------------------------------------------------------
gii = nb.load(FILE)

help(gii)

mgh_data = np.squeeze(np.asarray(mgh.dataobj))
nr_vertices = mgh_data.shape[0]


# print("Writing OBJ file...")
# basename = FILE.split(os.extsep, 1)[0]
# outname = "{}_bvbabel.obj".format(basename)
# bvbabel.obj.write_obj(outname, mesh_data["vertices"],
#                       mesh_data["vertex normals"],
#                       mesh_data["faces"])
#
# print("Finished.")
