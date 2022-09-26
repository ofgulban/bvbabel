"""Read, write, create BrainVoyager MTC file format."""

import struct
import numpy as np
from bvbabel.utils import read_variable_length_string, write_variable_length_string


# =============================================================================
def read_mtc(filename):
    """Read BrainVoyager MTC file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Pre-data headers.
    data : 2D numpy.array, (nr_vertices, time points)
        Vertex-wise time points (float32).

    """
    header = dict()
    data_mtc = dict()
    with open(filename, 'rb') as f:
        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["File version"] = data
        data, = struct.unpack('<i', f.read(4))
        header["Nr vertices"] = data
        data, = struct.unpack('<i', f.read(4))
        header["Nr time points"] = data

        # Expected binary data: variable-length string
        data = read_variable_length_string(f)
        header["VTC name"] = data
        data = read_variable_length_string(f)
        header["PRT name"] = data

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', f.read(1))
        header["Datatype (1 = float)"] = data

        # ---------------------------------------------------------------------
        # Vertex-wise time points data
        dims = (header["Nr vertices"], header["Nr time points"])
        data_mtc = np.fromfile(f, dtype='<f', count=dims[0]*dims[1], sep="",
                               offset=0)
        data_mtc = np.reshape(data_mtc, dims)

        return header, data_mtc


def write_mtc(filename, header, data_mtc):
    """Protocol to write BrainVoyager MTC file.

    Parameters
    ----------
    filename : string
        Path to file.
    header : dictionary
        Pre-data headers.
    data_mtc : 2D numpy.array, (nr_vertices, time points)
        Vertex-wise time points (float32).

    """
    with open(filename, 'wb') as f:
        # Expected binary data: int (4 bytes)
        data = header["File version"]
        f.write(struct.pack('<i', data))
        data = header["Nr vertices"]
        f.write(struct.pack('<i', data))
        data = header["Nr time points"]
        f.write(struct.pack('<i', data))

        # Expected binary data: variable-length string
        data = header["VTC name"]
        write_variable_length_string(f, data)
        data = header["PRT name"]
        write_variable_length_string(f, data)

        # Expected binary data: char (1 byte)
        data = header["Datatype (1 = float)"]
        f.write(struct.pack('<B', data))

        # ---------------------------------------------------------------------
        # Vertex-wise time points data
        dims = (header["Nr vertices"], header["Nr time points"])
        data_mtc = np.reshape(data_mtc, dims[0] * dims[1])
        for i in range(dims[0] * dims[1]):
            f.write(struct.pack('<f', data_mtc[i]))

        return header, data_mtc
