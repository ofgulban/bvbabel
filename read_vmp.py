"""Read BrainVoyager VMR file format."""

import struct
import numpy as np
import nibabel as nb

FILE = "/home/faruk/Documents/test_bvbabel/aseg_float_aligned.vmp"
OUT_NII = "/home/faruk/Documents/test_bvbabel/aseg_float_aligned.nii.gz"


def read_variable_length_string(reader):
    r"""Brainvoyager variable length strings terminate with b'\x00'."""
    text = ""
    data, = struct.unpack('<s', reader.read(1))
    while data != b'\x00':
        text += data.decode("utf-8")
        data = reader.read(1)
    return text


def read_RGB_bytes(reader):
    r"""Brainvoyager RGB bytes (unsigned char)."""
    RGB = np.zeros(3, dtype=np.ubyte)
    for i in range(3):
        data, = struct.unpack('<B', reader.read(1))
        RGB[i] = data
    return RGB


header = dict()
with open(FILE, 'rb') as reader:
    # -------------------------------------------------------------------------
    # NR-VMP Header (Version 6)
    # -------------------------------------------------------------------------

    # Expected binary data: int (4 bytes)
    data, = struct.unpack('<i', reader.read(4))
    header["NR-VMP identifier"] = data

    # Expected binary data: short int (2 bytes)
    data, = struct.unpack('<h', reader.read(2))
    header["VersionNumber"] = data
    data, = struct.unpack('<h', reader.read(2))
    header["DocumentType"] = data

    # Expected binary data: int (4 bytes)
    data, = struct.unpack('<i', reader.read(4))
    header["NrOfSubMaps"] = data
    data, = struct.unpack('<i', reader.read(4))
    header["NrOfTimePoints"] = data
    data, = struct.unpack('<i', reader.read(4))
    header["NrOfComponentParams"] = data
    data, = struct.unpack('<i', reader.read(4))
    header["ShowParamsRangeFrom"] = data
    data, = struct.unpack('<i', reader.read(4))
    header["ShowParamsRangeTo"] = data
    data, = struct.unpack('<i', reader.read(4))
    header["UseForFingerprintParamsRangeFrom"] = data
    data, = struct.unpack('<i', reader.read(4))
    header["UseForFingerprintParamsRangeTo"] = data

    data, = struct.unpack('<i', reader.read(4))
    header["XStart"] = data
    data, = struct.unpack('<i', reader.read(4))
    header["XEnd"] = data
    data, = struct.unpack('<i', reader.read(4))
    header["YStart"] = data
    data, = struct.unpack('<i', reader.read(4))
    header["YEnd"] = data
    data, = struct.unpack('<i', reader.read(4))
    header["ZStart"] = data
    data, = struct.unpack('<i', reader.read(4))
    header["ZEnd"] = data

    data, = struct.unpack('<i', reader.read(4))
    header["Resolution"] = data
    data, = struct.unpack('<i', reader.read(4))
    header["DimX"] = data
    data, = struct.unpack('<i', reader.read(4))
    header["DimY"] = data
    data, = struct.unpack('<i', reader.read(4))
    header["DimZ"] = data

    # Expected binary data: variable-length string
    data = read_variable_length_string(reader)
    header["NameOfVTCFile"] = data
    data = read_variable_length_string(reader)
    header["NameOfProtocolFile"] = data
    data = read_variable_length_string(reader)
    header["NameOfVOIFile"] = data

    header["Map"] = []
    for i in range(header["NrOfSubMaps"]):
        header["Map"].append(dict())

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][0]["TypeOfMap"] = data

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', reader.read(4))
        header["Map"][0]["MapThreshold"] = data
        data, = struct.unpack('<f', reader.read(4))
        header["Map"][0]["UpperThreshold"] = data

        # Expected binary data: variable-length string
        data = read_variable_length_string(reader)
        header["Map"][0]["MapName"] = data

        # Expected binary data: char (1 byte) x 3
        data = read_RGB_bytes(reader)
        header["Map"][0]["RGB positive min"] = data
        data = read_RGB_bytes(reader)
        header["Map"][0]["RGB positive max"] = data
        data = read_RGB_bytes(reader)
        header["Map"][0]["RGB negative min"] = data
        data = read_RGB_bytes(reader)
        header["Map"][0]["RGB negative max"] = data

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', reader.read(1))
        header["Map"][0]["UseVMPColor"] = data

        # Expected binary data: variable-length string
        data = read_variable_length_string(reader)
        header["Map"][0]["LUTFileName"] = data

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', reader.read(4))
        header["Map"][0]["TransparentColorFactor"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][0]["TransparentColorFactor"] = data
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][0]["DisplayMinLag"] = data
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][0]["DisplayMaxLag"] = data
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][0]["ShowCorrelationOrLag"] = data
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][0]["ClusterSizeThreshold"] = data

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<c', reader.read(1))
        header["Map"][0]["EnableClusterSizeThreshold"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][0]["ShowValuesAboveUpperThreshold"] = data
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][0]["DF1"] = data
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][0]["DF2"] = data

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<c', reader.read(1))
        header["Map"][0]["ShowPosNegValues"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][0]["NrOfUsedVoxels"] = data
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][0]["SizeOfFDRTable"] = data


# Print header information
for key, value in header.items():
    if key == "Map":
        for i, m in enumerate(value):
            print("Map index :", i)
            for map_key, map_value in m.items():
                print("    ", map_key, ":", map_value)
    else:
        print(key, ":", value)

# Test output data
# img_nii = nb.Nifti1Image(data, affine=np.eye(4))
# nb.save(img_nii, OUT_NII)
