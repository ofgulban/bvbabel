"""Read, write, create Brainvoyager SMP file format."""

import struct
import numpy as np
from bvbabel.utils import read_variable_length_string, read_RGB_bytes
from bvbabel.utils import write_variable_length_string, write_RGB_bytes


# =============================================================================
def read_smp(filename):
    """Read Brainvoyager SMP file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Header containing SMP information. See "Map" entry to reach information
        of individual maps. Such as their thresholds, color maps etc.
    data_smp : 2D numpy.array, [vertices, maps]
        Number of vertices is equal to the SRF on which the SMP is created.
        Each vertex has a number of values corresponding to maps in the header.

    """
    header = dict()
    with open(filename, 'rb') as f:
        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2))
        header["File version"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["Nr vertices"] = data

        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2))
        header["Nr maps"] = data

        # Expected binary data: variable length string
        data = read_variable_length_string(f)
        header["SRF name"] = data

        # NOTE(BV user guide): An SMP file may contain any statistic.
        #
        # BrainVoyager map type codes:
        # 1: T-statistic
        # 2: correlation
        # 3: cross-correlation
        # 4: F-statistic
        # 5: Z-statistic
        # 11: percent signal change
        # 12: ICA
        # 14: chi^2
        # 15: beta
        # 16: probability
        # 21: mean diffusivity map
        # 22: fractional anisotropy map

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["Map type"] = data

        data, = struct.unpack('<i', f.read(4))
        header["Nr lags"] = data
        data, = struct.unpack('<i', f.read(4))
        header["Min lag"] = data
        data, = struct.unpack('<i', f.read(4))
        header["Max lag"] = data
        data, = struct.unpack('<i', f.read(4))
        header["CC overlay"] = data
        data, = struct.unpack('<i', f.read(4))
        header["Cluster size"] = data

        if header["File version"] >= 2:
            # Expected binary data: char (1 byte)
            data, = struct.unpack('<B', f.read(1))
            header["Enable cluster check"] = data

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', f.read(4))
        header["Statistical threshold, critical value"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Statistical threshold, max value"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["Degrees of freedom, nominator if F-test"] = data
        data, = struct.unpack('<i', f.read(4))
        header["Degrees of freedom, denominator if F-test"] = data
        data, = struct.unpack('<i', f.read(4))
        header["Bonferroni correction value"] = data

        if header["File version"] >= 2:
            # Expected binary data: char (1 byte) x 3
            data = read_RGB_bytes(f)
            header["Critical value RGB"] = data
            data = read_RGB_bytes(f)
            header["Max value RGB"] = data

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', f.read(1))
        header["Enable SMP color"] = data

        if header["File version"] >= 2:
            # Expected binary data: float (4 bytes)
            data, = struct.unpack('<f', f.read(4))
            header["Color transparency"] = data

        # Expected binary data: variable length string
        data = read_variable_length_string(f)
        header["Map name"] = data

        # ---------------------------------------------------------------------
        # Read SMP data
        # ---------------------------------------------------------------------
        data_smp = np.zeros((header["Nr vertices"], header["Nr maps"]),
                            dtype=np.float32)
        for i in range(header["Nr maps"]):
            for j in range(header["Nr vertices"]):
                data, = struct.unpack('<f', f.read(4))
                data_smp[j, i] = data

    return header, data_smp


def write_smp(filename, header, data_smp):
    """Procecure to write Brainvoyager SMP file.

    Parameters
    ----------
    filename : string
        Path to file.
    header : dictionary
        Header containing SMP information. See "Map" entry to reach information
        of individual maps. Such as their thresholds, color maps etc.
    data_smp : 2D numpy.array, [vertices, maps]
        Number of vertices is equal to the SRF on which the SMP is created.
        Each vertex has a number of values corresponding to maps in the header.

    """
    with open(filename, 'wb') as f:
        # Expected binary data: short int (2 bytes)
        data = header["File version"]
        f.write(struct.pack('<h', data))

        # Expected binary data: int (4 bytes)
        data = header["Nr vertices"]
        f.write(struct.pack('<i', data))

        # Expected binary data: short int (2 bytes)
        data = header["Nr maps"]
        f.write(struct.pack('<h', data))

        # Expected binary data: variable length string
        data = header["SRF name"]
        write_variable_length_string(f, data)

        # Expected binary data: int (4 bytes)
        data = header["Map type"]
        f.write(struct.pack('<i', data))

        data = header["Nr lags"]
        f.write(struct.pack('<i', data))
        data = header["Min lag"]
        f.write(struct.pack('<i', data))
        data = header["Max lag"]
        f.write(struct.pack('<i', data))
        data = header["CC overlay"]
        f.write(struct.pack('<i', data))
        data = header["Cluster size"]
        f.write(struct.pack('<i', data))

        if header["File version"] >= 2:
            # Expected binary data: char (1 byte)
            data = header["Enable cluster check"]
            f.write(struct.pack('<B', data))

        # Expected binary data: float (4 bytes)
        data = header["Statistical threshold, critical value"]
        f.write(struct.pack('<f', data))
        data = header["Statistical threshold, max value"]
        f.write(struct.pack('<f', data))

        # Expected binary data: int (4 bytes)
        data = header["Degrees of freedom, nominator if F-test"]
        f.write(struct.pack('<i', data))
        data = header["Degrees of freedom, denominator if F-test"]
        f.write(struct.pack('<i', data))
        data = header["Bonferroni correction value"]
        f.write(struct.pack('<i', data))

        if header["File version"] >= 2:
            # Expected binary data: char (1 byte) x 3
            data = header["Critical value RGB"]
            write_RGB_bytes(f, data)
            data = header["Max value RGB"]
            write_RGB_bytes(f, data)

        # Expected binary data: char (1 byte)
        data = header["Enable SMP color"]
        f.write(struct.pack('<B', data))

        if header["File version"] >= 2:
            # Expected binary data: float (4 bytes)
            data = header["Color transparency"]
            f.write(struct.pack('<f', data))

        # Expected binary data: variable length string
        data = header["Map name"]
        write_variable_length_string(f, data)

        # ---------------------------------------------------------------------
        # Write SMP data
        # ---------------------------------------------------------------------
        for i in range(header["Nr maps"]):
            for j in range(header["Nr vertices"]):
                f.write(struct.pack('<f', data_smp[j, i]))
