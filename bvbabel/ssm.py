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
        TODO.
    data : 3D numpy.array
        TODO.

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
            data_ssm[i], = struct.unpack('<f', f.read(4))

    return header, data_ssm
