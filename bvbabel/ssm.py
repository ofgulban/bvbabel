"""Read, write, create BrainVoyager SSM file format."""

import struct
import numpy as np


# =============================================================================
def read_ssm(filename):
    """Read BrainVoyager SSM (surface to surface mapping) file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Header containing SMP information.
    data : 1D numpy.array
        Data containing vertex indices

    """
    header = dict()
    with open(filename, 'rb') as f:
        # ---------------------------------------------------------------------
        # Header
        # ---------------------------------------------------------------------
        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2))
        header["File version"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["Nr vertices 1"] = data
        data, = struct.unpack('<i', f.read(4))
        header["Nr vertices 2"] = data  # Referenced mesh number of vertices

        # ---------------------------------------------------------------------
        # Data
        # ---------------------------------------------------------------------
        data_ssm = np.zeros(header["Nr vertices 1"])
        for i in range(header["Nr vertices 1"]):
            data_ssm[i], = struct.unpack('<i', f.read(4))

    return header, data_ssm


def write_ssm(filename, header, data_ssm):
    """Protocol to write BrainVoyager SSM (surface to surface mapping) file.

    Parameters
    ----------
    filename : string
        Path to file.
    header : dictionary
        Header containing SMP information
    data_ssm : 1D numpy.array
        Data containing vertex indices

    """
    with open(filename, 'wb') as f:
        # ---------------------------------------------------------------------
        # Header
        # ---------------------------------------------------------------------
        # Expected binary data: short int (2 bytes)
        data = header["File version"]
        f.write(struct.pack('<h', data))

        # Expected binary data: int (4 bytes)
        data = header["Nr vertices 1"]
        f.write(struct.pack('<i', data))
        data = header["Nr vertices 2"]  # Referenced mesh number of vertices
        f.write(struct.pack('<i', data))

        # ---------------------------------------------------------------------
        # Data
        # ---------------------------------------------------------------------
        f.write(data_ssm.astype("<i").tobytes(order="C"))


def create_ssm(nr_vertices=32492):
    nr_vertices = int(nr_vertices)

    # Create header
    header = dict()
    header["File version"] = 2
    header["Nr vertices 1"] = nr_vertices
    header["Nr vertices 2"] = nr_vertices

    # Create data
    data_ssm = np.arange(1, nr_vertices+1)

    return header, data_ssm
