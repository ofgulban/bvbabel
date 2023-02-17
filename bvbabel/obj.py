"""Read, write, create Wevefront OBJ file format."""

import struct
import numpy as np


# =============================================================================
def write_obj(filename, vertices, vertex_normals, faces):
    """Protocol to write wavefront OBJ file.

    Parameters
    ----------
    filename : string
        Path to file.
    vertices : 2D numpy.array, (nr_vertices, XYZ coordinates)
        Vertex coordinates (float32).
    vertex_normals : 2D numpy.array, (nr_vertices, XYZ coordinates)
        Vertex normals (float32).
    faces : 2D numpy.array, (nr_vertices, vertex_indices)
        Faces (triangles), as indices of vertices (uint16).

    """
    nr_vertices = vertices.shape[0]
    nr_vertex_normals = vertex_normals.shape[0]
    nr_faces = faces.shape[0]

    with open(filename, 'w') as f:
        f.write("# Converted from BrainVoyager SRF format.\n")
        f.write("# Number of vertices: {}\n".format(nr_vertices))
        f.write("# Number of faces: {}\n".format(nr_faces))
        f.write("\n")

        f.write("# Vertex coordinates (x, y, z ,w)\n")
        for i in range(nr_vertices):
            f.write("v {} {} {} 1.0\n".format(vertices[i, 0],
                                              vertices[i, 1],
                                              vertices[i, 2]))
        f.write("\n")

        f.write("# Vertex normals (x, y, z)\n")
        for i in range(nr_vertex_normals):  # invert normal directions
            f.write("vn {} {} {}\n".format(vertex_normals[i, 0] * -1,
                                           vertex_normals[i, 1] * -1,
                                           vertex_normals[i, 2] * -1))
        f.write("\n")

        f.write("# Faces (indices start from 1)\n")
        for i in range(nr_faces):  # invert face winding
            f.write("f {} {} {}\n".format(faces[i, 2] + 1,
                                          faces[i, 1] + 1,
                                          faces[i, 0] + 1))
        f.write("\n")


def write_obj_colored(filename, vertices, vertex_normals, faces, vertex_colors):
    """Protocol to write wavefront OBJ file.

    Parameters
    ----------
    filename : string
        Path to file.
    vertices : 2D numpy.array, (nr_vertices, XYZ coordinates)
        Vertex coordinates (float32).
    vertex_normals : 2D numpy.array, (nr_vertices, XYZ coordinates)
        Vertex normals (float32).
    faces : 2D numpy.array, (nr_vertices, vertex_indices)
        Faces (triangles), as indices of vertices (uint16).
    vertex_colors : 2D numpy.array, (nr_vertices, RGBA coordinates)
        Vertex colors. Values are in between 0-1 (float32).

    """
    nr_vertices = vertices.shape[0]
    nr_vertex_normals = vertex_normals.shape[0]
    nr_faces = faces.shape[0]

    with open(filename, 'w') as f:
        f.write("# Converted from BrainVoyager SRF format.\n")
        f.write("# Number of vertices: {}\n".format(nr_vertices))
        f.write("# Number of faces: {}\n".format(nr_faces))
        f.write("\n")

        f.write("# Vertex coordinates (x, y, z ,w)\n")
        for i in range(nr_vertices):
            f.write("v {} {} {} {} {} {}\n".format(vertices[i, 0],
                                                   vertices[i, 1],
                                                   vertices[i, 2],
                                                   vertex_colors[i, 0],
                                                   vertex_colors[i, 1],
                                                   vertex_colors[i, 2]))
        f.write("\n")

        f.write("# Vertex normals (x, y, z)\n")
        for i in range(nr_vertex_normals):  # invert normal directions
            f.write("vn {} {} {}\n".format(vertex_normals[i, 0] * -1,
                                           vertex_normals[i, 1] * -1,
                                           vertex_normals[i, 2] * -1))
        f.write("\n")

        f.write("# Faces (indices start from 1)\n")
        for i in range(nr_faces):  # invert face winding
            f.write("f {} {} {}\n".format(faces[i, 2] + 1,
                                          faces[i, 1] + 1,
                                          faces[i, 0] + 1))
        f.write("\n")
