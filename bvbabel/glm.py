"""Read, write, create BrainVoyager GLM file format."""

import struct
import numpy as np
from bvbabel.utils import read_variable_length_string, read_RGB_bytes
from bvbabel.utils import write_variable_length_string, write_RGB_bytes


# =============================================================================
def read_glm(filename):
    """Read BrainVoyager GLM file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Pre-data headers.
    data : 3D numpy.array
        Image data.

    """
    header = dict()
    with open(filename, 'rb') as f:
        # ---------------------------------------------------------------------
        # GLM Header
        # ---------------------------------------------------------------------
        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2))
        header["File version"] = data

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', f.read(1))
        header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] = int(data)
        data, = struct.unpack('<B', f.read(1))
        header["RFX-GLM (0:std, 1:RFX)"] = int(data)

        # Random effects GLM
        if header["RFX-GLM (0:std, 1:RFX)"] == 1:
            # Expected binary data: int (4 bytes)
            data, = struct.unpack('<i', f.read(4))
            header["Nr subjects"] = data
            data, = struct.unpack('<i', f.read(4))
            header["Nr predictors per subject"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["Nr time points"] = data
        data, = struct.unpack('<i', f.read(4))
        header["Nr all predictors"] = data
        data, = struct.unpack('<i', f.read(4))
        header["Nr confound predictors"] = data
        data, = struct.unpack('<i', f.read(4))
        header["Nr studies"] = data

        if header["Nr studies"] > 1:
            data, = struct.unpack('<i', f.read(4))
            header["Nr studies with confound info"] = int(data)
            header["Nr confounds per study"] = []
            for j in range(header["Nr studies with confound info"]):
                data, = struct.unpack('<i', f.read(4))
                header["Nr confounds per study"].append(data)

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', f.read(1))
        header["Separate predictors (0:no, 1:studies, 2:subjects)"] = data
        data, = struct.unpack('<B', f.read(1))
        header["Time course normalization (1:z transform, 2:baseline z, 3:percent change)"] = data

        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2))
        header["Resolution (1, 2 or 3; with respect to VMR resolution)"] = data

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', f.read(1))
        header["Serial correlation(0:no, 1:AR(1), 2:AR(2))"] = data

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', f.read(4))
        header["Mean serial correlation before correction"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Mean serial correlation after correction"] = data

        # FMR-STC GLM
        if header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] == 0:
            # Expected binary data: short int (2 bytes)
            data, = struct.unpack('<h', f.read(2))
            header["DimX"] = data
            data, = struct.unpack('<h', f.read(2))
            header["DimY"] = data
            data, = struct.unpack('<h', f.read(2))
            header["DimZ"] = data

        # VMR-VTC GLM
        if header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] == 1:
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

        # SRF-MTC GLM
        if header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] == 2:
            # Expected binary data: int (4 bytes)
            data, = struct.unpack('<i', f.read(4))
            header["Nr vertices"] = data

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', f.read(1))
        header["Cortex-based mask (1:(grey matter) mask has been used)"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["Nr voxels in mask"] = data

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', f.read(1))


    return header
