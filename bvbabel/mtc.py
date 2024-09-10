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

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["Hemodynimic delay"] = data

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', f.read(4))
        header["TR"] = data
        data, = struct.unpack('<f', f.read(4))
        header["delta"] = data
        data, = struct.unpack('<f', f.read(4))
        header["tau"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["segment size"] = data
        data, = struct.unpack('<i', f.read(4))
        header["segment offset"] = data

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


# =============================================================================
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

        # Expected binary data: int (4 bytes)
        data = header["Hemodynimic delay"]
        f.write(struct.pack('<i', data))

        # Expected binary data: float (4 bytes)
        data = header["TR"]
        f.write(struct.pack('<f', data))
        data = header["delta"]
        f.write(struct.pack('<f', data))
        data = header["tau"]
        f.write(struct.pack('<f', data))

        # Expected binary data: int (4 bytes)
        data = header["segment size"]
        f.write(struct.pack('<i', data))
        data = header["segment offset"]
        f.write(struct.pack('<i', data))


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


# =============================================================================
def create_mtc():

    """Create BrainVoyager MTC file with default values."""

    header = dict()


    # -------------------------------------------------------------------------
    # NR-VMP Header (Version 1)
    # -------------------------------------------------------------------------

    # Expected binary data: int (4 bytes)
    header["File version"] = np.int32(1)
    header["Nr vertices"] = np.int32(3)
    header["Nr time points"] = np.int32(3) 

    # Expected binary data: variable-length string
    header["VTC name"] = " "
    header["PRT name"] = "<none>"

    # Expected binary data: int (4 bytes)
    header["Hemodynimic delay"] = np.int32(1)

    # Expected binary data: float (4 bytes)
    header["TR"] = np.float32(1)
    header["delta"] = np.float32(2.5)
    header["tau"] = np.float32(1.25)

    # Expected binary data: int (4 bytes)
    header["segment size"] = np.int32(10)
    header["segment offset"] = np.int32(0)

    # Expected binary data: char (1 byte)
    header["Datatype (1 = float)"] = np.byte(1)

    # ---------------------------------------------------------------------
    # Vertex-wise time points data
    data_mtc = np.random.random(np.prod((3,3))) * 2 - 1
    data_mtc = data_mtc.reshape((3,3))
    data_mtc = data_mtc.astype(np.float32)


    return header, data_mtc






