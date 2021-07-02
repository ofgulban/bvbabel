"""Read, write, create Brainvoyager SRF file format."""

import struct
import numpy as np

# =============================================================================
def read_srf(filename):
    """Read Brainvoyager SRF file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Pre-data and post-data headers.
    data : 3D numpy.array
        Triangular mesh data.

    """
    header = dict()
    with open(filename, 'rb') as f:
        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', f.read(4))
        header["File version"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["Reserved"] = data  # Must be '0'
        data, = struct.unpack('<i', f.read(4))
        header["Nr vertices"] = data
        data, = struct.unpack('<i', f.read(4))
        header["Nr triangles"] = data

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', f.read(4))
        header["Mesh center X"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Mesh center Y"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Mesh center Z"] = data

        # Vertex coordinates, Expected binary data: float (4 bytes)
        temp = np.zeros(header["Nr vertices"], dtype=np.float32)
        for i in range(header["Nr vertices"]):
            data, = struct.unpack('<f', f.read(4))
            temp[i] = data
        header["Vertex coord X"] = temp

        for i in range(header["Nr vertices"]):
            data, = struct.unpack('<f', f.read(4))
            temp[i] = data
        header["Vertex coord Y"] = temp

        for i in range(header["Nr vertices"]):
            data, = struct.unpack('<f', f.read(4))
            temp[i] = data
        header["Vertex coord Z"] = temp

        # Vertex normals, Expected binary data: float (4 bytes)
        for i in range(header["Nr vertices"]):
            data, = struct.unpack('<f', f.read(4))
            temp[i] = data
        header["Vertex normal X"] = temp

        for i in range(header["Nr vertices"]):
            data, = struct.unpack('<f', f.read(4))
            temp[i] = data
        header["Vertex normal Y"] = temp

        for i in range(header["Nr vertices"]):
            data, = struct.unpack('<f', f.read(4))
            temp[i] = data
        header["Vertex normal Z"] = temp

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', f.read(4))
        header["Vertex color convex curvature R"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Vertex color convex curvature G"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Vertex color convex curvature B"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Vertex color convex curvature A"] = data

        data, = struct.unpack('<f', f.read(4))
        header["Vertex color concave curvature R"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Vertex color concave curvature G"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Vertex color concave curvature B"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Vertex color concave curvature A"] = data

        # NOTE(Users Guide 2.3): MeshColor, sequence of color indices.
        # Each vertex has one color index. An index value of 0 references the
        # convex curvature color (stored after the normal vectors), a value of
        # 1 references the concave curvature color (stored after the convex
        # curvature color). Functional color look-up table values or RGB colors
        # can also be represented. An RGB color is identified by an index
        # value >= 1056964608. From the 4 byte index, the R, G and B component
        # can be extracted as third byte from the right, second byte from the
        # right and right most byte. These values are stored in a range from
        # 0 - 255. For OPenGL rendering, they have to be divided by 255.0.

        # Expected binary data: int (4 bytes)
        temp = np.zeros(header["Nr vertices"], dtype=np.int32)
        for i in range(header["Nr vertices"]):
            data, = struct.unpack('<i', f.read(4))
            temp[i] = data
        header["Mesh color index"] = temp
