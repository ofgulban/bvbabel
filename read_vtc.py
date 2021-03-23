"""Read BrainVoyager VMR file format."""

import struct
import numpy as np
import nibabel as nb

FILE = "/home/faruk/gdrive/test_bvbabel/S01_run1_sc.vtc"
OUT_NII = "/home/faruk/Documents/test_bvbabel/S01_run1_sc.nii.gz"

# =============================================================================
def read_variable_length_string(reader):
    r"""Brainvoyager variable length strings terminate with b'\x00'."""
    text = ""
    data, = struct.unpack('<s', reader.read(1))
    while data != b'\x00':
        text += data.decode("utf-8")
        data = reader.read(1)
    return text

# =============================================================================
header = dict()
with open(FILE, 'rb') as reader:

    # Expected binary data: short int (2 bytes)
    data, = struct.unpack('<h', reader.read(2))
    header["File version"] = data

    # Expected binary data: variable-length string
    data = read_variable_length_string(reader)
    header["Source FMR name"] = data

    # Expected binary data: short int (2 bytes)
    data, = struct.unpack('<h', reader.read(2))
    header["Nr of protocols (NP) attached to VTC"] = data

    if header["Nr of protocols (NP) attached to VTC"] > 0:
        # Expected binary data: variable-length string
        data = read_variable_length_string(reader)
        header["NP names"] = data
    else:
        header["NP names"] = ""

    # Expected binary data: short int (2 bytes)
    data, = struct.unpack('<h', reader.read(2))
    header["Current protocol index"] = data
    data, = struct.unpack('<h', reader.read(2))
    header["Data type of stored values (1:short int, 2:float)"] = data
    data, = struct.unpack('<h', reader.read(2))
    header["Nr time points"] = data
    data, = struct.unpack('<h', reader.read(2))
    header["Resolution relative to VMR (1, 2, or 3)"] = data

    data, = struct.unpack('<h', reader.read(2))
    header["XStart"] = data
    data, = struct.unpack('<h', reader.read(2))
    header["XEnd"] = data
    data, = struct.unpack('<h', reader.read(2))
    header["YStart"] = data
    data, = struct.unpack('<h', reader.read(2))
    header["YEnd"] = data
    data, = struct.unpack('<h', reader.read(2))
    header["ZStart"] = data
    data, = struct.unpack('<h', reader.read(2))
    header["ZEnd"] = data

    # Expected binary data: char (1 byte)
    data, = struct.unpack('<B', reader.read(1))
    header["L-R convention (0:unknown, 1:radiological, 2:neurological)"] = data
    data, = struct.unpack('<B', reader.read(1))
    header["Reference space (0:unknown, 1:native, 2:ACPC, 3:Tal)"] = data

    # Expected binary data: char (4 bytes)
    data, = struct.unpack('<f', reader.read(4))
    header["TR (ms)"] = data

    # -------------------------------------------------------------------------
    # Read VTC data
    # -------------------------------------------------------------------------
    # NOTE(Users Guide 2.3): Each data element (intensity value) is represented
    # in 2 bytes (unsigned short) or 4 bytes (float) as specified in the
    # "data type" entry. The data is organized in four loops:
    #   DimZ
    #       DimY
    #           DimX
    #               DimT

    # data = np.zeros((header["DimX"] * header["DimY"] * header["DimZ"]))
    # for i in range(data.size):
    #     data[i], = struct.unpack('<B', reader.read(1))
    # data = data.reshape((header["DimX"], header["DimY"], header["DimZ"]))


# Print header information
for key, value in header.items():
    print(key, ":", value)

# # Test output data
# img_nii = nb.Nifti1Image(data, affine=np.eye(4))
# nb.save(img_nii, OUT_NII)
