"""Read, write, create Brainvoyager MSK file format."""

import struct
import numpy as np

# =============================================================================
def read_msk(filename):
    """Read Brainvoyager MSK file.
    Parameters
    ----------
    filename : string
        Path to file.
    Returns
    -------
    header : dictionary
        Pre-data header.
    data : 3D numpy.array
        Image data.
    """
    header = dict()
    with open(filename, 'rb') as f:
        
        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2))
        header["VTC resolution relative to VMR (1, 2, or 3)"] = data
        
        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2))
        header["XStart"] = data
        data, = struct.unpack('<h', f.read(2))
        header["XEnd"] = data
        data, = struct.unpack('<h', f.read(2))
        header["YStart"] = data
        data, = struct.unpack('<h', f.read(2))
        header["YEnd"] = data
        data, = struct.unpack('<h', f.read(2))
        header["ZStart"] = data
        data, = struct.unpack('<h', f.read(2))
        header["ZEnd"] = data

        # Prepare dimensions of VTC data array
        VTC_resolution = header["VTC resolution relative to VMR (1, 2, or 3)"]
        DimX = (header["XEnd"] - header["XStart"]) // VTC_resolution
        DimY = (header["YEnd"] - header["YStart"]) // VTC_resolution
        DimZ = (header["ZEnd"] - header["ZStart"]) // VTC_resolution
        
        # ---------------------------------------------------------------------
        # Read MSK data
        # ---------------------------------------------------------------------
        
        data_img = np.zeros(DimZ * DimY * DimX)
        data_img = np.fromfile(f, dtype='<B', count=data_img.size, sep="", 
                               offset=0)
        data_img = np.reshape(data_img, (DimZ, DimY, DimX))
        data_img = np.transpose(data_img, (0, 2, 1))  # BV to Tal
        data_img = data_img[::-1, ::-1, ::-1]  # Flip BV axes

    return header, data_img


# =============================================================================
def write_msk(filename, header, data_img):
    """Protocol to write Brainvoyager MSK file.
    Parameters
    ----------
    filename : string
        Path to file.
    header : dictionary
        Pre-data header.
    data_img : 3D numpy.array
        Image data.
    """
    with open(filename, 'wb') as f:

        # Expected binary data: short int (2 bytes)
        data = header["VTC resolution relative to VMR (1, 2, or 3)"]
        f.write(struct.pack('<h', data))

        data = header["XStart"]
        f.write(struct.pack('<h', data))
        data = header["XEnd"]
        f.write(struct.pack('<h', data))
        data = header["YStart"]
        f.write(struct.pack('<h', data))
        data = header["YEnd"]
        f.write(struct.pack('<h', data))
        data = header["ZStart"]
        f.write(struct.pack('<h', data))
        data = header["ZEnd"]
        f.write(struct.pack('<h', data))

        # ---------------------------------------------------------------------
        # Write MSK data
        # ---------------------------------------------------------------------
        data_img = data_img[::-1, ::-1, ::-1]  # Flip BV axes
        data_img = np.transpose(data_img, (0, 2, 1))  # Tal to BV
        data_img = np.reshape(data_img, data_img.size)

        for i in range(data_img.size):
            f.write(struct.pack('<B', int(data_img[i])))