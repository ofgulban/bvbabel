"""Read, write, create BrainVoyager VTC file format."""

import struct
import numpy as np
from bvbabel.utils import read_variable_length_string
from bvbabel.utils import write_variable_length_string


# =============================================================================
def read_vtc(filename, rearrange_data_axes=True):
    """Read BrainVoyager VTC file.

    Parameters
    ----------
    filename : string
        Path to file.
    rearrange_data_axes : bool
        When 'False', axes are intended to follow LIP+ terminology used
        internally in BrainVoyager (however see the notes below):
            - 1st axis is Right to "L"eft.
            - 2nd axis is Superior to "I"nferior.
            - 3rd axis is Anterior to "P"osterior.
        When 'True' axes are intended to follow nibabel RAS+ terminology:
            - 1st axis is Left to "R"ight.
            - 2nd axis is Posterior to "A"nterior.
            - 3rd axis is Inferior to "S"uperior.

    Returns
    -------
    header : dictionary
        Pre-data and post-data headers.
    data : 3D numpy.array
        Image data.

    Notes
    -----
    - Based on several vtc inputs that are converted to nifti with RAS+ axes,
    I have concluded that the internal BrainVoyager axes are LIP+. However,
    this does not reflect the BrainVoyager VTC file documentation (Users Guide
    v2.3), in which the axes are described to be PIR+.
    - TODO[Faruk]: Revise the note below.
    Note that `ZStart - ZEnd` indicates the 1st data axis in the internal
    BrainVoyager PIR+ terminology. However `ZStart - ZEnd` indicates the
    3rd axis in RAS terminology. Time is in the 4th axis in both cases.


    """
    header = dict()
    with open(filename, 'rb') as f:
        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2))
        header["File version"] = data

        # Expected binary data: variable-length string
        data = read_variable_length_string(f)
        header["Source FMR name"] = data

        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2))
        header["Protocol attached"] = data

        if header["Protocol attached"] > 0:
            # Expected binary data: variable-length string
            data = read_variable_length_string(f)
            header["Protocol name"] = data
        else:
            header["Protocol name"] = ""

        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2))
        header["Current protocol index"] = data
        data, = struct.unpack('<h', f.read(2))
        header["Data type (1:short int, 2:float)"] = data
        data, = struct.unpack('<h', f.read(2))
        header["Nr time points"] = data
        data, = struct.unpack('<h', f.read(2))
        header["VTC resolution relative to VMR (1, 2, or 3)"] = data

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

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', f.read(1))
        header["L-R convention (0:unknown, 1:radiological, 2:neurological)"] = data
        data, = struct.unpack('<B', f.read(1))
        header["Reference space (0:unknown, 1:native, 2:ACPC, 3:Tal)"] = data

        # Expected binary data: char (4 bytes)
        data, = struct.unpack('<f', f.read(4))
        header["TR (ms)"] = data

        # ---------------------------------------------------------------------
        # Read VTC data
        # ---------------------------------------------------------------------
        # NOTE(Users Guide 2.3): Each data element (intensity value) is
        # represented in 2 bytes (unsigned short) or 4 bytes (float) as
        # specified in "data type" entry. The data is organized in four loops:
        #   DimZ
        #       DimY
        #           DimX
        #               DimT
        #
        # The axes terminology follows the internal BrainVoyager (BV) format.
        # The mapping to Talairach axes is as follows:
        #   BV (X front -> back) [axis 2 after np.reshape] = Y in Tal space
        #   BV (Y top -> bottom) [axis 1 after np.reshape] = Z in Tal space
        #   BV (Z left -> right) [axis 0 after np.reshape] = X in Tal space

        # Prepare dimensions of VTC data array
        VTC_resolution = header["VTC resolution relative to VMR (1, 2, or 3)"]
        DimX = (header["XEnd"] - header["XStart"]) // VTC_resolution
        DimY = (header["YEnd"] - header["YStart"]) // VTC_resolution
        DimZ = (header["ZEnd"] - header["ZStart"]) // VTC_resolution
        DimT = header["Nr time points"]

        data_img = np.zeros(DimZ * DimY * DimX * DimT)

        if header["Data type (1:short int, 2:float)"] == 1:
            data_img = np.fromfile(f, dtype='<h', count=data_img.size, sep="",
                                   offset=0)
        elif header["Data type (1:short int, 2:float)"] == 2:
            data_img = np.fromfile(f, dtype='<f', count=data_img.size, sep="",
                                   offset=0)
        else:
            raise("Unrecognized VTC data_img type.")

        data_img = np.reshape(data_img, (DimZ, DimY, DimX, DimT))

        # TODO[Faruk]: I need to triple check this part with various data
        if rearrange_data_axes is True:
            # TODO[Faruk] PIR+ to RAS+ ? I am not sure
            data_img = np.transpose(data_img, (0, 2, 1, 3))
            data_img = data_img[::-1, ::-1, ::-1, :]

    return header, data_img


# =============================================================================
def write_vtc(filename, header, data_img, rearrange_data_axes=True):
    """Protocol to write BrainVoyager VTC file.

    Parameters
    ----------
    filename : string
        Path to file.
    header : dictionary
        Pre-data and post-data headers.
    data_img : 3D numpy.array
        Image data.
    rearrange_data_axes : bool
        When 'False', axes are intended to follow LIP+ terminology used
        internally in BrainVoyager (however see the notes below):
            - 1st axis is Right to "L"eft.
            - 2nd axis is Superior to "I"nferior.
            - 3rd axis is Anterior to "P"osterior.
        When 'True' axes are intended to follow nibabel RAS+ terminology:
            - 1st axis is Left to "R"ight.
            - 2nd axis is Posterior to "A"nterior.
            - 3rd axis is Inferior to "S"uperior.

    """
    with open(filename, 'wb') as f:
        # Expected binary data: short int (2 bytes)
        data = header["File version"]
        f.write(struct.pack('<h', data))

        # Expected binary data: variable-length string
        data = header["Source FMR name"]
        write_variable_length_string(f, data)

        # Expected binary data: short int (2 bytes)
        data = header["Protocol attached"]
        f.write(struct.pack('<h', data))

        if header["Protocol attached"] > 0:
            # Expected binary data: variable-length string
            data = header["Protocol name"]
            write_variable_length_string(f, data)

        # Expected binary data: short int (2 bytes)
        data = header["Current protocol index"]
        f.write(struct.pack('<h', data))
        data = header["Data type (1:short int, 2:float)"]
        f.write(struct.pack('<h', data))
        data = header["Nr time points"]
        f.write(struct.pack('<h', data))
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

        # Expected binary data: char (1 byte)
        data = header["L-R convention (0:unknown, 1:radiological, 2:neurological)"]
        f.write(struct.pack('<B', data))
        data = header["Reference space (0:unknown, 1:native, 2:ACPC, 3:Tal)"]
        f.write(struct.pack('<B', data))

        # Expected binary data: char (4 bytes)
        data = header["TR (ms)"]
        f.write(struct.pack('<f', data))

        # ---------------------------------------------------------------------
        # Write VTC data
        # ---------------------------------------------------------------------
        if rearrange_data_axes is True:
            data_img = data_img[::-1, ::-1, ::-1, :]
            data_img = np.transpose(data_img, (0, 2, 1, 3))

        data_img = np.reshape(data_img, data_img.size)

        if header["Data type (1:short int, 2:float)"] == 1:
            for i in range(data_img.size):
                f.write(struct.pack('<h', data_img[i]))
        elif header["Data type (1:short int, 2:float)"] == 2:
            for i in range(data_img.size):
                f.write(struct.pack('<f', data_img[i]))
        else:
            raise("Unrecognized VTC data_img type.")


def create_vtc(rearrange_data_axes=True):
    """Create BrainVoyager VTC file with default values.

    Parameters
    ----------
    rearrange_data_axes : bool
        When 'False', axes are intended to follow LIP+ terminology used
        internally in BrainVoyager (however see the notes below):
            - 1st axis is Right to "L"eft.
            - 2nd axis is Superior to "I"nferior.
            - 3rd axis is Anterior to "P"osterior.
        When 'True' axes are intended to follow nibabel RAS+ terminology:
            - 1st axis is Left to "R"ight.
            - 2nd axis is Posterior to "A"nterior.
            - 3rd axis is Inferior to "S"uperior.

    """
    header = dict()
    # Expected binary data: short int (2 bytes)
    header["File version"] = 3

    # Expected binary data: variable-length string
    header["Source FMR name"] = ""

    # Expected binary data: short int (2 bytes)
    header["Protocol attached"] = 0

    # if header["Protocol attached"] > 0:
    #     # Expected binary data: variable-length string
    #     data = header["Protocol name"]
    #     write_variable_length_string(f, data)

    # Expected binary data: short int (2 bytes)
    header["Current protocol index"] = 0

    # NOTE: float vtc does not seem to work in BV so I make it short int
    header["Data type (1:short int, 2:float)"] = 1
    header["Nr time points"] = 10
    header["VTC resolution relative to VMR (1, 2, or 3)"] = 1

    header["XStart"] = 90
    header["XEnd"] = 210
    header["YStart"] = 100
    header["YEnd"] = 200
    header["ZStart"] = 110
    header["ZEnd"] = 190

    # Expected binary data: char (1 byte)
    header["L-R convention (0:unknown, 1:radiological, 2:neurological)"] = 1
    header["Reference space (0:unknown, 1:native, 2:ACPC, 3:Tal)"] = 1

    # Expected binary data: char (4 bytes)
    header["TR (ms)"] = 1000

    # -------------------------------------------------------------------------
    # Create data
    DimX = header["XEnd"] - header["XStart"]
    DimY = header["YEnd"] - header["YStart"]
    DimZ = header["ZEnd"] - header["ZStart"]
    DimT = header["Nr time points"]
    if rearrange_data_axes is True:
        dims = [DimX, DimY, DimZ, DimT]
    else:
        dims = [DimZ, DimY, DimX, DimT]
    data = np.random.random(np.prod(dims)) * 225  # 225 for BV visualization
    data = data.reshape(dims)
    data = data.astype(np.short)  # NOTE: float vtc does not seem to work in BV

    return header, data
