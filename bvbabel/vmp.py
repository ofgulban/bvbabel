"""Read, write, create BrainVoyager VMP file format."""

import struct
import numpy as np
from bvbabel.utils import read_variable_length_string, read_RGB_bytes
from bvbabel.utils import write_variable_length_string, write_RGB_bytes


# =============================================================================
def read_vmp(filename):
    """Read BrainVoyager VMP file.

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
        # NR-VMP Header (Version 6)
        # ---------------------------------------------------------------------

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["NR-VMP identifier"] = data

        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2))
        header["VersionNumber"] = data
        data, = struct.unpack('<h', f.read(2))
        header["DocumentType"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["NrOfSubMaps"] = int(data)  # number of sub-maps/component maps
        data, = struct.unpack('<i', f.read(4))
        header["NrOfTimePoints"] = int(data)
        data, = struct.unpack('<i', f.read(4))
        header["NrOfComponentParams"] = data
        data, = struct.unpack('<i', f.read(4))
        header["ShowParamsRangeFrom"] = data
        data, = struct.unpack('<i', f.read(4))
        header["ShowParamsRangeTo"] = data
        data, = struct.unpack('<i', f.read(4))
        header["UseForFingerprintParamsRangeFrom"] = data
        data, = struct.unpack('<i', f.read(4))
        header["UseForFingerprintParamsRangeTo"] = data

        data, = struct.unpack('<i', f.read(4))
        header["XStart"] = data
        data, = struct.unpack('<i', f.read(4))
        header["XEnd"] = data
        data, = struct.unpack('<i', f.read(4))
        header["YStart"] = data
        data, = struct.unpack('<i', f.read(4))
        header["YEnd"] = data
        data, = struct.unpack('<i', f.read(4))
        header["ZStart"] = data
        data, = struct.unpack('<i', f.read(4))
        header["ZEnd"] = data

        data, = struct.unpack('<i', f.read(4))
        header["Resolution"] = data
        data, = struct.unpack('<i', f.read(4))
        header["DimX"] = data
        data, = struct.unpack('<i', f.read(4))
        header["DimY"] = data
        data, = struct.unpack('<i', f.read(4))
        header["DimZ"] = data

        # Expected binary data: variable-length string
        data = read_variable_length_string(f)
        header["NameOfVTCFile"] = data
        data = read_variable_length_string(f)
        header["NameOfProtocolFile"] = data
        data = read_variable_length_string(f)
        header["NameOfVOIFile"] = data

        # Store each map as a dictionary element of a list
        header["Map"] = []
        for m in range(header["NrOfSubMaps"]):
            header["Map"].append(dict())

            # Expected binary data: int (4 bytes)
            data, = struct.unpack('<i', f.read(4))
            header["Map"][m]["TypeOfMap"] = data

            # Expected binary data: float (4 bytes)
            data, = struct.unpack('<f', f.read(4))
            header["Map"][m]["MapThreshold"] = data
            data, = struct.unpack('<f', f.read(4))
            header["Map"][m]["UpperThreshold"] = data

            # Expected binary data: variable-length string
            data = read_variable_length_string(f)
            header["Map"][m]["MapName"] = data

            # Expected binary data: char (1 byte) x 3
            data = read_RGB_bytes(f)
            header["Map"][m]["RGB positive min"] = data
            data = read_RGB_bytes(f)
            header["Map"][m]["RGB positive max"] = data
            data = read_RGB_bytes(f)
            header["Map"][m]["RGB negative min"] = data
            data = read_RGB_bytes(f)
            header["Map"][m]["RGB negative max"] = data

            # Expected binary data: char (1 byte)
            data, = struct.unpack('<B', f.read(1))
            header["Map"][m]["UseVMPColor"] = data

            # Expected binary data: variable-length string
            data = read_variable_length_string(f)
            header["Map"][m]["LUTFileName"] = data

            # Expected binary data: float (4 bytes)
            data, = struct.unpack('<f', f.read(4))
            header["Map"][m]["TransparentColorFactor"] = data

            # Expected binary data: int (4 bytes)
            if header["Map"][m]["TypeOfMap"] == 3:  # cross-correlation values
                data, = struct.unpack('<i', f.read(4))
                header["Map"][m]["NrOfLags"] = data
                data, = struct.unpack('<i', f.read(4))
                header["Map"][m]["DisplayMinLag"] = data
                data, = struct.unpack('<i', f.read(4))
                header["Map"][m]["DisplayMaxLag"] = data
                data, = struct.unpack('<i', f.read(4))
                header["Map"][m]["ShowCorrelationOrLag"] = data
            data, = struct.unpack('<i', f.read(4))
            header["Map"][m]["ClusterSizeThreshold"] = data

            # Expected binary data: char (1 byte)
            data, = struct.unpack('<b', f.read(1))
            header["Map"][m]["EnableClusterSizeThreshold"] = data

            # Expected binary data: int (4 bytes)
            data, = struct.unpack('<i', f.read(4))
            header["Map"][m]["ShowValuesAboveUpperThreshold"] = data
            data, = struct.unpack('<i', f.read(4))
            header["Map"][m]["DF1"] = data
            data, = struct.unpack('<i', f.read(4))
            header["Map"][m]["DF2"] = data

            # Expected binary data: char (1 byte)
            data, = struct.unpack('<b', f.read(1))
            header["Map"][m]["ShowPosNegValues"] = data

            # Expected binary data: int (4 bytes)
            data, = struct.unpack('<i', f.read(4))
            header["Map"][m]["NrOfUsedVoxels"] = data
            data, = struct.unpack('<i', f.read(4))
            header["Map"][m]["SizeOfFDRTable"] = data

            # Expected binary data: float (4 bytes) x SizeOfFDRTable x 3
            # (q, crit std, crit conservative)
            # TODO: Check FDR Tables
            temp = np.zeros((header["Map"][m]["SizeOfFDRTable"], 3))
            for i in range(header["Map"][m]["SizeOfFDRTable"]):
                for j in range(3):
                    data, = struct.unpack('<f', f.read(4))
                    temp[i, j] = data
            header["Map"][m]["FDRTableInfo"] = temp

            # Expected binary data: int (4 bytes)
            data, = struct.unpack('<i', f.read(4))
            header["Map"][m]["UseFDRTableIndex"] = data

            # Time course values associated with component "c"
            if header["NrOfTimePoints"] > 0:
                header["ComponentTimeCourseValues"] = []
                for i in range(header["NrOfSubMaps"]):
                    data = np.zeros(header["NrOfTimePoints"])
                    for j in range(header["NrOfTimePoints"]):
                        data[j], = struct.unpack('<f', f.read(4))
                    header["ComponentTimeCourseValues"].append(data)

            # Component parameters
            if header["NrOfComponentParams"] > 0:
                header["ComponentTimeCourseParams"] = []
                for i in range(header["NrOfComponentParams"]):
                    header["ComponentTimeCourseParams"].append(dict())

                    name = read_variable_length_string(f)
                    header["ComponentTimeCourseParams"][i]["Name"] = name

                    for j in range(header["NrOfSubMaps"]):
                        data, = struct.unpack('<f', f.read(4))
                        header["ComponentTimeCourseParams"][i]["Values"].append(data)

        # ---------------------------------------------------------------------
        # Read VMP image data
        # ---------------------------------------------------------------------
        # NOTE(Users Guide 2.3): A NR-VMP file contains DimN = NrOfSubMaps 3D
        # data sets. Each data set contains a 3D representation of a
        # (statistical) entity. Each data element (single value) is represented
        # in float format (4 bytes per value). The data is organized in four
        # loops:
        #   DimN (number of components/maps)
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

        data_img = np.fromfile(f, dtype='<f', count=data_img.size, sep="",
                               offset=0)

        if DimT > 1:  # Multiple maps
            data_img = np.reshape(data_img, (DimT, DimZ, DimY, DimX))
            data_img = np.transpose(data_img, (1, 3, 2, 0))  # BV to Tal
            data_img = data_img[::-1, ::-1, ::-1, :]  # Flip BV axes
        else:  # Single map
            data_img = np.reshape(data_img, (DimZ, DimY, DimX))
            data_img = np.transpose(data_img, (0, 2, 1))  # BV to Tal
            data_img = data_img[::-1, ::-1, ::-1]  # Flip BV axes
            # -----------------------------------------------------------------
            # NOTE[Faruk]: Single map solution for Kenshu. I did not encounter 
            # VMP files of lags that has multiple maps inside for now.
            if header["Map"][0]["TypeOfMap"] == 3:
                # NOTE[Faruk]: It seems that lag are coded in the integers and 
                # correlation coefficient is coded in decimals. 
                data_lag = np.floor(data_img)
                data_corr = data_img % 1
                data_img = np.stack((data_lag, data_corr), axis=3)
            # -----------------------------------------------------------------

    return header, data_img


# =============================================================================
def write_vmp(filename, header, data_img):
    """Protocol to write BrainVoyager VMP file.

    Parameters
    ----------
    filename : string
        Path to file.
    header : dictionary
        Pre-data and post-data headers.
    data_img : 3D numpy.array
        Image data.

    """
    with open(filename, 'wb') as f:
        # ---------------------------------------------------------------------
        # NR-VMP Header (Version 6)
        # ---------------------------------------------------------------------

        # Expected binary data: int (4 bytes)
        data = header["NR-VMP identifier"]
        f.write(struct.pack('<i', data))

        # Expected binary data: short int (2 bytes)
        data = header["VersionNumber"]
        f.write(struct.pack('<h', data))
        data = header["DocumentType"]
        f.write(struct.pack('<h', data))

        # Expected binary data: int (4 bytes)
        data = header["NrOfSubMaps"]  # number of sub-maps/component maps
        f.write(struct.pack('<i', data))
        data = header["NrOfTimePoints"]
        f.write(struct.pack('<i', data))
        data = header["NrOfComponentParams"]
        f.write(struct.pack('<i', data))
        data = header["ShowParamsRangeFrom"]
        f.write(struct.pack('<i', data))
        data = header["ShowParamsRangeTo"]
        f.write(struct.pack('<i', data))
        data = header["UseForFingerprintParamsRangeFrom"]
        f.write(struct.pack('<i', data))
        data = header["UseForFingerprintParamsRangeTo"]
        f.write(struct.pack('<i', data))

        data = header["XStart"]
        f.write(struct.pack('<i', data))
        data = header["XEnd"]
        f.write(struct.pack('<i', data))
        data = header["YStart"]
        f.write(struct.pack('<i', data))
        data = header["YEnd"]
        f.write(struct.pack('<i', data))
        data = header["ZStart"]
        f.write(struct.pack('<i', data))
        data = header["ZEnd"]
        f.write(struct.pack('<i', data))

        data = header["Resolution"]
        f.write(struct.pack('<i', data))
        data = header["DimX"]
        f.write(struct.pack('<i', data))
        data = header["DimY"]
        f.write(struct.pack('<i', data))
        data = header["DimZ"]
        f.write(struct.pack('<i', data))

        # Expected binary data: variable-length string
        data = header["NameOfVTCFile"]
        write_variable_length_string(f, data)
        data = header["NameOfProtocolFile"]
        write_variable_length_string(f, data)
        data = header["NameOfVOIFile"]
        write_variable_length_string(f, data)

        # Store each map as a dictionary element of a list
        for m in range(header["NrOfSubMaps"]):

            # Expected binary data: int (4 bytes)
            data = header["Map"][m]["TypeOfMap"]
            f.write(struct.pack('<i', data))

            # Expected binary data: float (4 bytes)
            data = header["Map"][m]["MapThreshold"]
            f.write(struct.pack('<f', data))
            data = header["Map"][m]["UpperThreshold"]
            f.write(struct.pack('<f', data))

            # Expected binary data: variable-length string
            write_variable_length_string(f, header["Map"][m]["MapName"])

            # Expected binary data: char (1 byte) x 3
            data = header["Map"][m]["RGB positive min"]
            write_RGB_bytes(f, data)
            data = header["Map"][m]["RGB positive max"]
            write_RGB_bytes(f, data)
            data = header["Map"][m]["RGB negative min"]
            write_RGB_bytes(f, data)
            data = header["Map"][m]["RGB negative max"]
            write_RGB_bytes(f, data)

            # Expected binary data: char (1 byte)
            data = header["Map"][m]["UseVMPColor"]
            f.write(struct.pack('<B', data))

            # Expected binary data: variable-length string
            data = header["Map"][m]["LUTFileName"]
            write_variable_length_string(f, data)

            # Expected binary data: float (4 bytes)
            data = header["Map"][m]["TransparentColorFactor"]
            f.write(struct.pack('<f', data))

            # Expected binary data: int (4 bytes)
            if header["Map"][m]["TypeOfMap"] == 3:  # cross-correlation values
                data = header["Map"][m]["NrOfLags"]
                f.write(struct.pack('<i', data))
                data = header["Map"][m]["DisplayMinLag"]
                f.write(struct.pack('<i', data))
                data = header["Map"][m]["DisplayMaxLag"]
                f.write(struct.pack('<i', data))
                data = header["Map"][m]["ShowCorrelationOrLag"]
                f.write(struct.pack('<i', data))
            data = header["Map"][m]["ClusterSizeThreshold"]
            f.write(struct.pack('<i', data))

            # Expected binary data: char (1 byte)
            data = header["Map"][m]["EnableClusterSizeThreshold"]
            f.write(struct.pack('<b', data))

            # Expected binary data: int (4 bytes)
            data = header["Map"][m]["ShowValuesAboveUpperThreshold"]
            f.write(struct.pack('<i', data))
            data = header["Map"][m]["DF1"]
            f.write(struct.pack('<i', data))
            data = header["Map"][m]["DF2"]
            f.write(struct.pack('<i', data))

            # Expected binary data: char (1 byte)
            data = header["Map"][m]["ShowPosNegValues"]
            f.write(struct.pack('<b', data))

            # Expected binary data: int (4 bytes)
            data = header["Map"][m]["NrOfUsedVoxels"]
            f.write(struct.pack('<i', data))
            data = header["Map"][m]["SizeOfFDRTable"]
            f.write(struct.pack('<i', data))

            # Expected binary data: float (4 bytes) x SizeOfFDRTable x 3
            # (q, crit std, crit conservative)
            # TODO: Check FDR Tables
            data = header["Map"][m]["FDRTableInfo"]
            for i in range(header["Map"][m]["SizeOfFDRTable"]):
                for j in range(3):
                    f.write(struct.pack('<f', data[i, j]))

            # Expected binary data: int (4 bytes)
            data = header["Map"][m]["UseFDRTableIndex"]
            f.write(struct.pack('<i', data))

            # Time course values associated with component "c"
            if header["NrOfTimePoints"] > 0:
                data = header["ComponentTimeCourseValues"]
                for i in range(header["NrOfSubMaps"]):
                    for j in range(header["NrOfTimePoints"]):
                        f.write(struct.pack('<f', data[i, j]))

            # Component parameters
            if header["NrOfComponentParams"] > 0:
                for i in range(header["NrOfComponentParams"]):
                    name = header["ComponentTimeCourseParams"][i]["Name"]
                    write_variable_length_string(f, name)

                    data = header["ComponentTimeCourseParams"][i]["Values"]
                    for j in range(header["NrOfSubMaps"]):
                        f.write(struct.pack('<f', data[j]))

        # ---------------------------------------------------------------------
        # Write VMP image data
        # ---------------------------------------------------------------------
        if header["NrOfSubMaps"] > 1:  # Multiple maps
            data_img = data_img[::-1, ::-1, ::-1, :]  # Flip BV axes
            data_img = np.transpose(data_img, (3, 0, 2, 1))  # TAL to BV
            data_img = np.reshape(data_img, data_img.size)
        else:  # Single maps
            # -----------------------------------------------------------------
            # NOTE[Faruk]: Single map solution for Kenshu. I did not encounter 
            # VMP files of lags that has multiple maps inside for now.
            if header["Map"][0]["TypeOfMap"] == 3:
                # NOTE[Faruk]: It seems that lag are coded in the integers and 
                # correlation coefficient is coded in decimals. 
                data_img = data_img[:, :, :, 0] + data_img[:, :, :, 1]
            # -----------------------------------------------------------------

            data_img = data_img[::-1, ::-1, ::-1]  # Flip BV axes
            data_img = np.transpose(data_img, (0, 2, 1))  # TAL to BV
            data_img = np.reshape(data_img, data_img.size)
        f.write(data_img.astype("<f").tobytes(order="C"))


# =============================================================================
def create_vmp():
    """Create BrainVoyager VMP file with default values."""

    header = dict()
    # -------------------------------------------------------------------------
    # NR-VMP Header (Version 6)
    # -------------------------------------------------------------------------

    # Expected binary data: int (4 bytes)
    header["NR-VMP identifier"] = np.int32(-1582119980)

    # Expected binary data: short int (2 bytes)
    header["VersionNumber"] = np.int16(6)
    header["DocumentType"] = np.int16(1)

    # Expected binary data: int (4 bytes)
    header["NrOfSubMaps"] = np.int32(1)
    header["NrOfTimePoints"] = np.int32(0)
    header["NrOfComponentParams"] = np.int32(0)
    header["ShowParamsRangeFrom"] = np.int32(0)
    header["ShowParamsRangeTo"] = np.int32(0)
    header["UseForFingerprintParamsRangeFrom"] = np.int32(0)
    header["UseForFingerprintParamsRangeTo"] = np.int32(0)
    header["XStart"] = np.int32(0)
    header["XEnd"] = np.int32(256)
    header["YStart"] = np.int32(0)
    header["YEnd"] = np.int32(256)
    header["ZStart"] = np.int32(0)
    header["ZEnd"] = np.int32(256)
    header["Resolution"] = np.int32(1)
    header["DimX"] = np.int32(256)
    header["DimY"] = np.int32(256)
    header["DimZ"] = np.int32(256)

    # Expected binary data: variable-length string
    header["NameOfVTCFile"] = ""
    header["NameOfProtocolFile"] = ""
    header["NameOfVOIFile"] = ""

    # -------------------------------------------------------------------------
    # Map information
    # -------------------------------------------------------------------------
    header["Map"] = list()
    header["Map"].append(dict())

    # Expected binary data: int (4 bytes)
    header["Map"][0]["TypeOfMap"] = np.int32(1)

    # Expected binary data: float (4 bytes)
    header["Map"][0]["MapThreshold"] = np.float32(0.5)
    header["Map"][0]["UpperThreshold"] = np.float32(1)

    # Expected binary data: variable-length string
    header["Map"][0]["MapName"] = "bvbabel default random numbers"

    # Expected binary data: char (1 byte) x 3
    header["Map"][0]["RGB positive min"] = np.array([224, 243, 248], dtype=np.ubyte)
    header["Map"][0]["RGB positive max"] = np.array([ 40,  51, 144], dtype=np.ubyte)
    header["Map"][0]["RGB negative min"] = np.array([254, 236, 153], dtype=np.ubyte)
    header["Map"][0]["RGB negative max"] = np.array([145,   0,  37], dtype=np.ubyte)

    # Expected binary data: char (1 byte)
    header["Map"][0]["UseVMPColor"] = np.byte(0)

    # Expected binary data: variable-length string
    header["Map"][0]["LUTFileName"] = "<default>"

    # Expected binary data: float (4 bytes)
    header["Map"][0]["TransparentColorFactor"] = np.float32(1.0)

    # Expected binary data: int (4 bytes)
    header["Map"][0]["ClusterSizeThreshold"] = np.int32(1)

    # Expected binary data: char (1 byte)
    header["Map"][0]["EnableClusterSizeThreshold"] = np.byte(0)

    # Expected binary data: int (4 bytes)
    header["Map"][0]["ShowValuesAboveUpperThreshold"] = np.int32(1)
    header["Map"][0]["DF1"] = np.int32(0)
    header["Map"][0]["DF2"] = np.int32(0)

    # Expected binary data: char (1 byte)
    header["Map"][0]["ShowPosNegValues"] = np.byte(3)

    # Expected binary data: int (4 bytes)
    header["Map"][0]["NrOfUsedVoxels"] = np.int32(0)
    header["Map"][0]["SizeOfFDRTable"] = np.int32(0)

    # Expected binary data: float (4 bytes) x SizeOfFDRTable x 3
    # (q, crit std, crit conservative)
    # TODO: Check FDR Tables
    header["Map"][0]["FDRTableInfo"] = np.int32(0)

    # Expected binary data: int (4 bytes)
    header["Map"][0]["UseFDRTableIndex"] = np.int32(0)

    # -------------------------------------------------------------------------
    # Create random data
    # -------------------------------------------------------------------------
    dims = [header["DimZ"], header["DimY"], header["DimX"]]
    data = np.random.random(np.prod(dims)) * 2 - 1
    data = data.reshape(dims)
    data = data.astype(np.float32)

    return header, data