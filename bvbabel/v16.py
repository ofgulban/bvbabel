"""Read, write, create Brainvoyager V16 file format."""

import struct
import numpy as np
from bvbabel.utils import (read_variable_length_string,
                           write_variable_length_string)


# =============================================================================
def read_v16(filename):
    """Read Brainvoyager V16 file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Pre-data and post-data headers.
    data : 3D numpy.array
        Image data.

    """
    header = dict()
    with open(filename, 'rb') as f:
        # ---------------------------------------------------------------------
        # V16 Pre-Data Header
        # ---------------------------------------------------------------------
        # NOTE: V16 files contain anatomical 3D data sets,
        # typically containing the whole brain (head) of subjects. The
        # intensity values are stored as a series of bytes. The V16 format
        # stores each intensity value with two bytes (short integers). The V16
        # format contains a small header followed by the actual data. V16
        # files do not contain a post-data header and have no file version

        # Expected binary data: unsigned short int (2 bytes)
        data, = struct.unpack('<H', f.read(2))
        header["DimX"] = data
        data, = struct.unpack('<H', f.read(2))
        header["DimY"] = data
        data, = struct.unpack('<H', f.read(2))
        header["DimZ"] = data

        # ---------------------------------------------------------------------
        # V16 Data
        # ---------------------------------------------------------------------
        # NOTE(Developer Guide 2.6): Each data element (intensity value) is
        # represented in 1 byte. The data is organized in three loops:
        #   DimZ
        #       DimY
        #           DimX
        #
        # The axes terminology follows the internal BrainVoyager (BV) format.
        # The mapping to Talairach axes is as follows:
        #   BV (X front -> back) [axis 2 after np.reshape] = Y in Tal space
        #   BV (Y top -> bottom) [axis 1 after np.reshape] = Z in Tal space
        #   BV (Z left -> right) [axis 0 after np.reshape] = X in Tal space

        # Expected binary data: unsigned short (2 bytes)
        data_img = np.zeros((header["DimZ"] * header["DimY"] * header["DimX"]),
                            dtype='<H')
        data_img = np.fromfile(f, dtype='<H', count=data_img.size, sep="",
                               offset=0)
        data_img = np.reshape(
            data_img, (header["DimZ"], header["DimY"], header["DimX"]))

        data_img = np.transpose(data_img, (0, 2, 1))  # BV to Tal
        data_img = data_img[::-1, ::-1, ::-1]  # Flip BV axes

    return header, data_img


# =============================================================================
def write_v16(filename, header, data_img):
    """Protocol to write Brainvoyager V16 file.

    Parameters
    ----------
    filename : string
        Output filename.
    header : dictionary
        Header of V16 file (vmr headers are also accepted).
    data_img : numpy.array, 3D
        Image.

    """
    with open(filename, 'wb') as f:
        # ---------------------------------------------------------------------
        # V16 Pre-Data Header
        # ---------------------------------------------------------------------
        # Expected binary data: unsigned short int (2 bytes)
        data = header["DimX"]
        f.write(struct.pack('<H', data))
        data = header["DimY"]
        f.write(struct.pack('<H', data))
        data = header["DimZ"]
        f.write(struct.pack('<H', data))

        # ---------------------------------------------------------------------
        # V16 Data
        # ---------------------------------------------------------------------
        # Convert axes from Nifti standard back to BV standard
        data_img = data_img[::-1, ::-1, ::-1]  # Flip BV axes
        data_img = np.transpose(data_img, (0, 2, 1))  # BV to Tal

        # Expected binary data: unsigned short (2 bytes)
        data_img = data_img.flatten()
        for i in range(data_img.size):
            f.write(struct.pack('<H', data_img[i]))

    return print("V16 saved.")


def create_v16():
    """Create Brainvoyager V16 file with default values."""
    header = dict()
    # Expected binary data: unsigned short int (2 bytes)
    header["DimX"] = 256
    header["DimY"] = 256
    header["DimZ"] = 256

    # -------------------------------------------------------------------------
    # Create data
    dims = [header["DimX"], header["DimY"], header["DimZ"]]
    data = np.random.randint(0, high=65535, size=dims, dtype=np.uint16)
    data = data.reshape(dims)

    return header, data
