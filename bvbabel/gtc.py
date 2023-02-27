"""Read, write, create BrainVoyager GTC file format."""

import struct
import numpy as np


# =============================================================================
def read_gtc(filename):
    """Read BrainVoyager GTC file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Pre-data header.
    data_img : 4D numpy.array, (depth, x, y, time)
        Depth grid sampled images with time course.

    """
    header = dict()
    with open(filename, 'rb') as f:
        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["File version"] = data

        data, = struct.unpack('<i', f.read(4))
        header["DimD"] = data
        data, = struct.unpack('<i', f.read(4))
        header["DimX"] = data
        data, = struct.unpack('<i', f.read(4))
        header["DimY"] = data
        data, = struct.unpack('<i', f.read(4))
        header["DimT"] = data

        # ---------------------------------------------------------------------
        # Read GTC data
        # ---------------------------------------------------------------------
        # The data is organized in four loops:
        #   DimD
        #       DimY
        #           DimX
        #               DimT
        data_img = np.zeros(header["DimD"] * header["DimY"] * header["DimX"]
                            * header["DimT"], dtype=np.int32)
        data_img = np.fromfile(f, dtype='<i', count=data_img.size, sep="",
                               offset=0)

        # Rearrange data
        data_img = np.reshape(data_img, (header["DimD"], header["DimY"],
                              header["DimX"], header["DimT"]))
        data_img = np.transpose(data_img, (2, 1, 0, 3))

        return header, data_img


# =============================================================================
def write_gtc(filename, header, data_img):
    """Protocol to write BrainVoyager GTC file.

    Parameters
    ----------
    filename : string
        Path to file.
    header : dictionary
        Pre-data header.
    data_img : 4D numpy.array, (depth, x, y, time)
        Depth grid sampled images with time course.

    """
    with open(filename, 'wb') as f:
        # Expected binary data: int (4 bytes)
        data = header["File version"]
        f.write(struct.pack('<i', data))

        data = header["DimD"]
        f.write(struct.pack('<i', data))
        data = header["DimX"]
        f.write(struct.pack('<i', data))
        data = header["DimY"]
        f.write(struct.pack('<i', data))
        data = header["DimT"]
        f.write(struct.pack('<i', data))

        # ---------------------------------------------------------------------
        # Write GTC data
        # ---------------------------------------------------------------------
        data_img = np.transpose(data_img, (2, 1, 0, 3))
        data_img = np.reshape(data_img, data_img.size)
        f.write(data_img.astype("<i").tobytes(order="C"))
