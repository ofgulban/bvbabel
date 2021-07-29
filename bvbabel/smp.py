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

    Notes
    -----
    An SMP file may contain any statistic. See some of Brain Voyager map codes:
        1: T-statistic, 2: Correlation, 3: Cross-correlation, 4: F-statistic
        5: Z-statistic, 11: Percent signal change, 12: ICA, 14: Chi^2, 15: Beta
        16: Probability, 21: Mean diffusivity, 22: Fractional anisotropy,
        25: Polar angle

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

        # ---------------------------------------------------------------------
        data_smp = np.zeros((header["Nr vertices"], header["Nr maps"]),
                            dtype=np.float32)  # Prepare data array
        header["Map"] = []
        for m in range(header["Nr maps"]):
            header["Map"].append(dict())

            # Expected binary data: int (4 bytes)
            data, = struct.unpack('<i', f.read(4))
            header["Map"][m]["Map type"] = data

            # Read additional values only if a lag map
            if header["File version"] >= 3 and header["Map"][m]["Map type"] == 3:
                data, = struct.unpack('<i', f.read(4))
                header["Map"][m]["CC nr lags"] = data
                data, = struct.unpack('<i', f.read(4))
                header["Map"][m]["CC min lag"] = data
                data, = struct.unpack('<i', f.read(4))
                header["Map"][m]["CC max lag"] = data
                data, = struct.unpack('<i', f.read(4))
                header["Map"][m]["CC overlay"] = data
            else:
                header["Map"][m]["Nr lags"] = 0
                header["Map"][m]["CC min lag"] = 0
                header["Map"][m]["CC max lag"] = 0
                header["Map"][m]["CC overlay"] = 0

            data, = struct.unpack('<i', f.read(4))
            header["Map"][m]["Cluster size"] = data

            # Expected binary data: char (1 byte)
            data, = struct.unpack('<B', f.read(1))
            header["Map"][m]["Cluster checkbox"] = data

            # Expected binary data: float (4 bytes)
            data, = struct.unpack('<f', f.read(4))
            header["Map"][m]["Threshold min"] = data
            data, = struct.unpack('<f', f.read(4))
            header["Map"][m]["Threshold max"] = data

            if header["File version"] >= 4:
                # Expected binary data: int (4 bytes)
                data, = struct.unpack('<i', f.read(4))
                header["Map"][m]["Threshold include greater than max"] = data

            # Expected binary data: int (4 bytes)
            data, = struct.unpack('<i', f.read(4))
            header["Map"][m]["Degrees of freedom, nominator if F-test"] = data
            data, = struct.unpack('<i', f.read(4))
            header["Map"][m]["Degrees of freedom, denominator if F-test"] = data

            if header["File version"] >= 5:
                # Expected binary data: int (4 bytes)
                data, = struct.unpack('<i', f.read(4))
                header["Map"][m]["Show positive negative"] = data
            else:
                header["Map"][m]["Show positive negative"] = 3

            data, = struct.unpack('<i', f.read(4))
            header["Map"][m]["Bonferroni correction value"] = data

            if header["File version"] >= 2:
                # Expected binary data: char (1 byte) x 3
                data = read_RGB_bytes(f)
                header["Map"][m]["RGB positive min"] = data
                data = read_RGB_bytes(f)
                header["Map"][m]["RGB positive max"] = data

                if header["File version"] >= 4:
                    data = read_RGB_bytes(f)
                    header["Map"][m]["RGB negative min"] = data
                    data = read_RGB_bytes(f)
                    header["Map"][m]["RGB negative max"] = data

                # Expected binary data: char (1 byte)
                data, = struct.unpack('<B', f.read(1))
                header["Map"][m]["RGB or LUT"] = data

                if header["File version"] >= 5:
                    # Expected binary data: variable length string
                    data = read_variable_length_string(f)
                    header["Map"][m]["LUT file"] = data
                else:
                    header["Map"][m]["LUT file"] = "<default>"

                # Expected binary data: float (4 bytes)
                data, = struct.unpack('<f', f.read(4))
                header["Map"][m]["Color transparency"] = data

            # Expected binary data: variable length string
            data = read_variable_length_string(f)
            header["Map"][m]["Map name"] = data

            # -----------------------------------------------------------------
            # Read SMP data
            # -----------------------------------------------------------------
            for v in range(header["Nr vertices"]):
                data, = struct.unpack('<f', f.read(4))
                data_smp[v, m] = data

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
