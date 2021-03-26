"""Read BrainVoyager VMP file format."""

import struct
import numpy as np
import nibabel as nb

FILE = "/home/faruk/Documents/test_bvbabel/sub-01_ses-01_RightHand.vmp"
OUT_NII = "/home/faruk/Documents/test_bvbabel/sub-01_ses-01_RightHand_bvbabel.nii.gz"


# =============================================================================
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


def read_float_array(reader, nr_floats):
    r"""Read multiple floats into 1D numpy array."""
    out_data = np.zeros(nr_floats, dtype=np.float)
    for i in range(nr_floats):
        data, = struct.unpack('<f', reader.read(4))
        out_data[i] = data
    return out_data


# =============================================================================
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
    header["NrOfSubMaps"] = data  # number of sub-maps/component maps
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

    # Store each map as a dictionary element of a list
    header["Map"] = []
    for m in range(header["NrOfSubMaps"]):
        header["Map"].append(dict())

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][m]["TypeOfMap"] = data

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', reader.read(4))
        header["Map"][m]["MapThreshold"] = data
        data, = struct.unpack('<f', reader.read(4))
        header["Map"][m]["UpperThreshold"] = data

        # Expected binary data: variable-length string
        data = read_variable_length_string(reader)
        header["Map"][m]["MapName"] = data

        # Expected binary data: char (1 byte) x 3
        data = read_RGB_bytes(reader)
        header["Map"][m]["RGB positive min"] = data
        data = read_RGB_bytes(reader)
        header["Map"][m]["RGB positive max"] = data
        data = read_RGB_bytes(reader)
        header["Map"][m]["RGB negative min"] = data
        data = read_RGB_bytes(reader)
        header["Map"][m]["RGB negative max"] = data

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', reader.read(1))
        header["Map"][m]["UseVMPColor"] = data

        # Expected binary data: variable-length string
        data = read_variable_length_string(reader)
        header["Map"][m]["LUTFileName"] = data

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', reader.read(4))
        header["Map"][m]["TransparentColorFactor"] = data

        # Expected binary data: int (4 bytes)
        if header["Map"][m]["TypeOfMap"] == 3:  # cross-correlation values
            data, = struct.unpack('<i', reader.read(4))
            header["Map"][m]["NrOfLags"] = data
            data, = struct.unpack('<i', reader.read(4))
            header["Map"][m]["DisplayMinLag"] = data
            data, = struct.unpack('<i', reader.read(4))
            header["Map"][m]["DisplayMaxLag"] = data
            data, = struct.unpack('<i', reader.read(4))
            header["Map"][m]["ShowCorrelationOrLag"] = data
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][m]["ClusterSizeThreshold"] = data

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<b', reader.read(1))
        header["Map"][m]["EnableClusterSizeThreshold"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][m]["ShowValuesAboveUpperThreshold"] = data
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][m]["DF1"] = data
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][m]["DF2"] = data

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<b', reader.read(1))
        header["Map"][m]["ShowPosNegValues"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][m]["NrOfUsedVoxels"] = data
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][m]["SizeOfFDRTable"] = data

        # Expected binary data: float (4 bytes) x SizeOfFDRTable x 3
        # (q, crit std, crit conservative)
        # TODO: Check FDR Tables
        temp = np.zeros((header["Map"][m]["SizeOfFDRTable"], 3))
        for i in range(header["Map"][m]["SizeOfFDRTable"]):
            for j in range(3):
                data, = struct.unpack('<f', reader.read(4))
                temp[i, j] = data
        header["Map"][m]["FDRTableInfo"] = temp

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', reader.read(4))
        header["Map"][m]["UseFDRTableIndex"] = data

        # Time course values associated with component "c"
        # NOTE(Faruk): I dont really understand the use-case of this. I need an
        # example VMP that has this field to test it.
        if header["NrOfTimePoints"] > 0:
            header["ComponentTimeCourseValues"] = []
            for i in range(header["NrOfSubMaps"]):
                data = np.zeros(header["NrOfTimePoints"])
                for j in range(header["NrOfTimePoints"]):
                    data[j], = struct.unpack('<f', reader.read(4))
                header["ComponentTimeCourseValues"].append(data)

        # Component parameters
        if header["NrOfComponentParams"] > 0:
            header["ComponentTimeCourseParams"] = []
            for i in range(header["NrOfComponentParams"]):
                name = read_variable_length_string(reader)
                header[name] = []
                for j in range(header["NrOfSubMaps"]):
                    data, = struct.unpack('<f', reader.read(4))
                    header[name].append(data)

    # -------------------------------------------------------------------------
    # Read VMP image data
    # -------------------------------------------------------------------------
    # NOTE(Users Guide 2.3): A NR-VMP file contains DimN = NrOfSubMaps 3D data
    # sets. Each data set contains a 3D representation of a (statistical)
    # entity. Each data element (single value) is represented in float format
    # (4 bytes per value). The data is organized in four loops:
    #   DimN (NrOfComponents)
    #       DimZ
    #           DimY
    #               DimX
    #
    # The axes terminology follows the internal BrainVoyager (BV) format.
    # The mapping to Talairach axes is as follows:
    #   BV (X front -> back) [axis 2 after np.reshape] = Y in Tal space
    #   BV (Y top -> bottom) [axis 1 after np.reshape] = Z in Tal space
    #   BV (Z left -> right) [axis 0 after np.reshape] = X in Tal space
    VMP_resolution = header["Resolution"]
    DimX = (header["XEnd"] - header["XStart"]) // VMP_resolution
    DimY = (header["YEnd"] - header["YStart"]) // VMP_resolution
    DimZ = (header["ZEnd"] - header["ZStart"]) // VMP_resolution
    DimT = header["NrOfSubMaps"]
    data_img = np.zeros(DimT * DimZ * DimY * DimX)
    for i in range(data_img.size):
        data_img[i], = struct.unpack('<f', reader.read(4))
    data_img = np.reshape(data_img, (DimT, DimZ, DimY, DimX))
    data_img = np.transpose(data_img, (1, 3, 2, 0))  # BV to Tal
    data_img = data_img[::-1, ::-1, ::-1, :]  # Flip BV axes

# Print header information
for key, value in header.items():
    if key == "Map":
        for i, m in enumerate(value):
            print("Map index :", i)
            for map_key, map_value in m.items():
                print("  ", map_key, ":", map_value)
    else:
        print(key, ":", value)

# Test output data
img_nii = nb.Nifti1Image(data_img, affine=np.eye(4))
nb.save(img_nii, OUT_NII)
