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
    data_smp : 2D numpy.array, [nr vertices, nr maps]
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
        header["SRF file"] = data

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

            # NOTE(BV Documentation): Degrees of freedom 1 is nominator if
            # F-test. Degrees of freedom 1 is denominator if F-test.
            # Expected binary data: int (4 bytes)
            data, = struct.unpack('<i', f.read(4))
            header["Map"][m]["Degrees of freedom 1"] = data
            data, = struct.unpack('<i', f.read(4))
            header["Map"][m]["Degrees of freedom 2"] = data

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
            header["Map"][m]["Name"] = data

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
    data_smp : 2D numpy.array, [nr vertices, nr maps]
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
        data = header["SRF file"]
        write_variable_length_string(f, data)

        # ---------------------------------------------------------------------
        for m in range(header["Nr maps"]):
            # Expected binary data: int (4 bytes)
            data = header["Map"][m]["Map type"]
            f.write(struct.pack('<i', data))

            if header["File version"] >= 3 and header["Map"][m]["Map type"] == 3:
                data = header["Map"][m]["CC nr lags"]
                f.write(struct.pack('<i', data))
                data = header["Map"][m]["CC min lag"]
                f.write(struct.pack('<i', data))
                data = header["Map"][m]["CC max lag"]
                f.write(struct.pack('<i', data))
                data = header["Map"][m]["CC overlay"]
                f.write(struct.pack('<i', data))

            data = header["Map"][m]["Cluster size"]
            f.write(struct.pack('<i', data))

            # Expected binary data: char (1 byte)
            data = header["Map"][m]["Cluster checkbox"]
            f.write(struct.pack('<B', data))

            # Expected binary data: float (4 bytes)
            data = header["Map"][m]["Threshold min"]
            f.write(struct.pack('<f', data))
            data = header["Map"][m]["Threshold max"]
            f.write(struct.pack('<f', data))

            if header["File version"] >= 4:
                # Expected binary data: int (4 bytes)
                data = header["Map"][m]["Threshold include greater than max"]
                f.write(struct.pack('<i', data))

            # Expected binary data: int (4 bytes)
            data = header["Map"][m]["Degrees of freedom 1"]
            f.write(struct.pack('<i', data))
            data = header["Map"][m]["Degrees of freedom 2"]
            f.write(struct.pack('<i', data))
            data = header["Map"][m]["Show positive negative"]
            f.write(struct.pack('<i', data))
            data = header["Map"][m]["Bonferroni correction value"]
            f.write(struct.pack('<i', data))

            if header["File version"] >= 2:
                # Expected binary data: char (1 byte) x 3
                data = header["Map"][m]["RGB positive min"]
                write_RGB_bytes(f, data)
                data = header["Map"][m]["RGB positive max"]
                write_RGB_bytes(f, data)

                if header["File version"] >= 4:
                    data = header["Map"][m]["RGB negative min"]
                    write_RGB_bytes(f, data)
                    data = header["Map"][m]["RGB negative max"]
                    write_RGB_bytes(f, data)

                # Expected binary data: char (1 byte)
                data = header["Map"][m]["RGB or LUT"]
                f.write(struct.pack('<B', data))

                # Expected binary data: variable length string
                data = header["Map"][m]["LUT file"]
                write_variable_length_string(f, data)

                # Expected binary data: float (4 bytes)
                data = header["Map"][m]["Color transparency"]
                f.write(struct.pack('<f', data))

            # Expected binary data: variable length string
            data = header["Map"][m]["Name"]
            write_variable_length_string(f, data)

            # -----------------------------------------------------------------
            # Write SMP data
            # -----------------------------------------------------------------
            for v in range(header["Nr vertices"]):
                f.write(struct.pack('<f', data_smp[v, m]))


def create_smp(nr_maps=1, nr_vertices=64000):
    """Create Brainvoyager SMP file with default values."""
    nr_vertices = int(nr_vertices)
    nr_maps = int(nr_maps)

    header = dict()
    # Expected binary data: short int (2 bytes)
    header["File version"] = 5
    # Expected binary data: int (4 bytes)
    header["Nr vertices"] = nr_vertices
    # Expected binary data: short int (2 bytes)
    header["Nr maps"] = nr_maps
    # Expected binary data: variable length string
    header["SRF file"] = ""

    header["Map"] = list()
    for m in range(int(nr_maps)):
        header["Map"].append(dict())
        header["Map"][m]["Map type"] = 15
        header["Map"][m]["Cluster size"] = 4
        header["Map"][m]["Cluster checkbox"] = 0
        header["Map"][m]["Threshold min"] = 0.001
        header["Map"][m]["Threshold max"] = 1.
        header["Map"][m]["Threshold include greater than max"] = 1

        # Expected binary data: int (4 bytes)
        header["Map"][m]["Degrees of freedom 1"] = 100
        header["Map"][m]["Degrees of freedom 2"] = 0
        header["Map"][m]["Show positive negative"] = 3
        header["Map"][m]["Bonferroni correction value"] = nr_vertices
        header["Map"][m]["RGB positive min"] = np.array([1, 1, 1], dtype=np.uint8)
        header["Map"][m]["RGB positive max"] = np.array([255, 1, 1], dtype=np.uint8)
        header["Map"][m]["RGB negative min"] = np.array([1, 1, 1], dtype=np.uint8)
        header["Map"][m]["RGB negative max"] = np.array([1, 1, 255], dtype=np.uint8)

        # Expected binary data: char (1 byte)
        header["Map"][m]["RGB or LUT"] = 0
        # Expected binary data: variable length string
        header["Map"][m]["LUT file"] = "<default>"
        # Expected binary data: float (4 bytes)
        header["Map"][m]["Color transparency"] = 1.0
        # Expected binary data: variable length string
        header["Map"][m]["Name"] = "Map {}".format(nr_maps)

        # Create data
        data = np.ones((nr_vertices, nr_maps), dtype=np.float32)
        data[0:nr_vertices//2] = 0.5

    return header, data
