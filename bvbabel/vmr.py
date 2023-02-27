"""Read, write, create BrainVoyager VMR file format."""

import struct
import numpy as np
from bvbabel.utils import (read_variable_length_string,
                           write_variable_length_string)


# =============================================================================
def read_vmr(filename):
    """Read BrainVoyager VMR file.

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
        # VMR Pre-Data Header
        # ---------------------------------------------------------------------
        # NOTE(Developer Guide 2.6): VMR files contain anatomical 3D data sets,
        # typically containing the whole brain (head) of subjects. The
        # intensity values are stored as a series of bytes. See the V16 format
        # for a version storing each intensity value with two bytes (short
        # integers). The VMR format contains a small header followed by the
        # actual data followed by a second, more extensive, header. The current
        # version of VMR files is "4", which is only slightly different from
        # version 3 (as indicated below). Version 3 added offset values to
        # format 2 in order to represent large data sets efficiently, e.g. in
        # the context of advanced segmentation processing. Compared to the
        # original file version "1", file versions 2 and higher contain
        # additional header information after the actual data ("post-data
        # header"). This allows to read VMR data sets with minimal header
        # checking if the extended information is not needed. The information
        # in the post-data header contains position information (if available)
        # and stores a series of spatial transformations, which might have been
        # performed to the original data set ("history record"). The
        # post-header data can be probably ignored for custom routines, but is
        # important in BrainVoyager QX for spatial transformation and
        # coregistration routines as well as for proper visualization.

        # Expected binary data: unsigned short int (2 bytes)
        data, = struct.unpack('<H', f.read(2))
        header["File version"] = data
        data, = struct.unpack('<H', f.read(2))
        header["DimX"] = data
        data, = struct.unpack('<H', f.read(2))
        header["DimY"] = data
        data, = struct.unpack('<H', f.read(2))
        header["DimZ"] = data

        # ---------------------------------------------------------------------
        # VMR Data
        # ---------------------------------------------------------------------
        # NOTE(Developer Guide 2.6): Each data element (intensity value) is
        # represented in 1 byte. The data is organized in three loops:
        #   DimZ
        #       DimY
        #           DimX
        #
        # The axes terminology follows the internal BrainVoyager (BV) format.
        # The mapping to Talairach axes is as follows:
        #   BV (X front -> back) [axis 2 after np.reshape] = Y in Tal space
        #   BV (Y top -> bottom) [axis 1 after np.reshape] = Z in Tal space
        #   BV (Z left -> right) [axis 0 after np.reshape] = X in Tal space

        # Expected binary data: unsigned char (1 byte)
        data_img = np.zeros((header["DimZ"] * header["DimY"] * header["DimX"]),
                            dtype='<B')
        data_img = np.fromfile(f, dtype='<B', count=data_img.size, sep="",
                               offset=0)
        data_img = np.reshape(
            data_img, (header["DimZ"], header["DimY"], header["DimX"]))

        data_img = np.transpose(data_img, (0, 2, 1))  # BV to Tal
        data_img = data_img[::-1, ::-1, ::-1]  # Flip BV axes

        # ---------------------------------------------------------------------
        # VMR Post-Data Header
        # ---------------------------------------------------------------------
        # NOTE(Developer Guide 2.6): The first four entries of the post-data
        # header are new since file version "3" and contain offset values for
        # each dimension as well as a value indicating the size of a cube with
        # iso-dimensions to which the data set will be internally "expanded"
        # for certain operations. The axes labels are in terms of
        # BrainVoyager's internal format. These four entries are followed by
        # scan position information from the original file headers, e.g. from
        # DICOM files. The coordinate axes labels in these entries are not in
        # terms of BrainVoyager's internal conventions but follow the DICOM
        # standard. Then follows eventually a section listing spatial
        # transformations which have been eventually performed to create the
        # current VMR (e.g. ACPC transformation). Finally, additional
        # information further descries the data set, including the assumed
        # left-right convention, the reference space (e.g. Talairach after
        # normalization) and voxel resolution.

        if header["File version"] >= 3:
            # NOTE(Developer Guide 2.6): These four entries have been added in
            # file version "3" with BrainVoyager QX 1.7. All other entries are
            # identical to file version "2".

            # Expected binary data: short int (2 bytes)
            data, = struct.unpack('<h', f.read(2))
            header["OffsetX"] = data
            data, = struct.unpack('<h', f.read(2))
            header["OffsetY"] = data
            data, = struct.unpack('<h', f.read(2))
            header["OffsetZ"] = data
            data, = struct.unpack('<h', f.read(2))
            header["FramingCubeDim"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["PosInfosVerified"] = data
        data, = struct.unpack('<i', f.read(4))
        header["CoordinateSystem"] = data

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', f.read(4))
        header["Slice1CenterX"] = data  # First slice center X coordinate
        data, = struct.unpack('<f', f.read(4))
        header["Slice1CenterY"] = data  # First slice center Y coordinate
        data, = struct.unpack('<f', f.read(4))
        header["Slice1CenterZ"] = data  # First slice center Z coordinate
        data, = struct.unpack('<f', f.read(4))
        header["SliceNCenterX"] = data  # Last slice center X coordinate
        data, = struct.unpack('<f', f.read(4))
        header["SliceNCenterY"] = data  # Last slice center Y coordinate
        data, = struct.unpack('<f', f.read(4))
        header["SliceNCenterZ"] = data  # Last slice center Z coordinate
        data, = struct.unpack('<f', f.read(4))
        header["RowDirX"] = data  # Slice row direction vector X component
        data, = struct.unpack('<f', f.read(4))
        header["RowDirY"] = data  # Slice row direction vector Y component
        data, = struct.unpack('<f', f.read(4))
        header["RowDirZ"] = data  # Slice row direction vector Z component
        data, = struct.unpack('<f', f.read(4))
        header["ColDirX"] = data  # Slice column direction vector X component
        data, = struct.unpack('<f', f.read(4))
        header["ColDirY"] = data  # Slice column direction vector Y component
        data, = struct.unpack('<f', f.read(4))
        header["ColDirZ"] = data  # Slice column direction vector Z component

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["NRows"] = data  # Nr of rows of slice image matrix
        data, = struct.unpack('<i', f.read(4))
        header["NCols"] = data  # Nr of columns of slice image matrix

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', f.read(4))
        header["FoVRows"] = data  # Field of view extent in row direction [mm]
        data, = struct.unpack('<f', f.read(4))
        header["FoVCols"] = data  # Field of view extent in column dir. [mm]
        data, = struct.unpack('<f', f.read(4))
        header["SliceThickness"] = data  # Slice thickness [mm]
        data, = struct.unpack('<f', f.read(4))
        header["GapThickness"] = data  # Gap thickness [mm]

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["NrOfPastSpatialTransformations"] = data

        if header["NrOfPastSpatialTransformations"] != 0:
            # NOTE(Developer Guide 2.6): For each past transformation, the
            # information specified in the following table is stored. The
            # "type of transformation" is a value determining how many
            # subsequent values define the transformation:
            #   "1": Rigid body+scale (3 translation, 3 rotation, 3 scale)
            #   "2": Affine transformation (16 values, 4x4 matrix)
            #   "4": Talairach transformation
            #   "5": Un-Talairach transformation (1 - 5 -> BV axes)
            header["PastTransformation"] = []
            for i in range(header["NrOfPastSpatialTransformations"]):
                header["PastTransformation"].append(dict())

                # Expected binary data: variable-length string
                data = read_variable_length_string(f)
                header["PastTransformation"][i]["Name"] = data

                # Expected binary data: int (4 bytes)
                data, = struct.unpack('<i', f.read(4))
                header["PastTransformation"][i]["Type"] = data

                # Expected binary data: variable-length string
                data = read_variable_length_string(f)
                header["PastTransformation"][i]["SourceFileName"] = data

                # Expected binary data: int (4 bytes)
                data, = struct.unpack('<i', f.read(4))
                header["PastTransformation"][i]["NrOfValues"] = data

                # Store transformation values as a list
                trans_values = []
                for j in range(header["PastTransformation"][i]["NrOfValues"]):
                    # Expected binary data: float (4 bytes)
                    data, = struct.unpack('<f', f.read(4))
                    trans_values.append(data)
                header["PastTransformation"][i]["Values"] = trans_values

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', f.read(1))
        header["LeftRightConvention"] = data  # modified in v4

        if header["File version"] >= 4:
            data, = struct.unpack('<B', f.read(1))
            header["ReferenceSpaceVMR"] = data  # new in v4

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', f.read(4))
        header["VoxelSizeX"] = data  # Voxel resolution along X axis
        data, = struct.unpack('<f', f.read(4))
        header["VoxelSizeY"] = data  # Voxel resolution along Y axis
        data, = struct.unpack('<f', f.read(4))
        header["VoxelSizeZ"] = data  # Voxel resolution along Z axis

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', f.read(1))
        header["VoxelResolutionVerified"] = data
        data, = struct.unpack('<B', f.read(1))
        header["VoxelResolutionInTALmm"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["VMROrigV16MinValue"] = data  # 16-bit data min intensity
        data, = struct.unpack('<i', f.read(4))
        header["VMROrigV16MeanValue"] = data  # 16-bit data mean intensity
        data, = struct.unpack('<i', f.read(4))
        header["VMROrigV16MaxValue"] = data  # 16-bit data max intensity

    return header, data_img


# =============================================================================
def write_vmr(filename, header, data_img):
    """Protocol to write BrainVoyager VMR file.

    Parameters
    ----------
    filename : string
        Output filename.
    header : dictionary
        Header of VMR file.
    data_img : numpy.array, 3D
        Image.

    """
    with open(filename, 'wb') as f:
        # ---------------------------------------------------------------------
        # VMR Pre-Data Header
        # ---------------------------------------------------------------------
        # Expected binary data: unsigned short int (2 bytes)
        data = header["File version"]
        f.write(struct.pack('<H', data))
        data = header["DimX"]
        f.write(struct.pack('<H', data))
        data = header["DimY"]
        f.write(struct.pack('<H', data))
        data = header["DimZ"]
        f.write(struct.pack('<H', data))

        # ---------------------------------------------------------------------
        # VMR Data
        # ---------------------------------------------------------------------
        # Convert axes from Nifti standard back to BV standard
        data_img = data_img[::-1, ::-1, ::-1]  # Flip BV axes
        data_img = np.transpose(data_img, (0, 2, 1))  # BV to Tal

        # Expected binary data: unsigned char (1 or 2 byte)
        f.write(data_img.astype("<B").tobytes(order="C"))

        # ---------------------------------------------------------------------
        # VMR Post-Data Header
        # ---------------------------------------------------------------------
        if header["File version"] >= 3:
            # Expected binary data: short int (2 bytes)
            data = header["OffsetX"]
            f.write(struct.pack('<h', data))
            data = header["OffsetY"]
            f.write(struct.pack('<h', data))
            data = header["OffsetZ"]
            f.write(struct.pack('<h', data))
            data = header["FramingCubeDim"]
            f.write(struct.pack('<h', data))

        # Expected binary data: int (4 bytes)
        data = header["PosInfosVerified"]
        f.write(struct.pack('<i', data))
        data = header["CoordinateSystem"]
        f.write(struct.pack('<i', data))

        # Expected binary data: float (4 bytes)
        data = header["Slice1CenterX"]
        f.write(struct.pack('<f', data))
        data = header["Slice1CenterY"]
        f.write(struct.pack('<f', data))
        data = header["Slice1CenterZ"]
        f.write(struct.pack('<f', data))
        data = header["SliceNCenterX"]
        f.write(struct.pack('<f', data))
        data = header["SliceNCenterY"]
        f.write(struct.pack('<f', data))
        data = header["SliceNCenterZ"]
        f.write(struct.pack('<f', data))
        data = header["RowDirX"]
        f.write(struct.pack('<f', data))
        data = header["RowDirY"]
        f.write(struct.pack('<f', data))
        data = header["RowDirZ"]
        f.write(struct.pack('<f', data))
        data = header["ColDirX"]
        f.write(struct.pack('<f', data))
        data = header["ColDirY"]
        f.write(struct.pack('<f', data))
        data = header["ColDirZ"]
        f.write(struct.pack('<f', data))

        # Expected binary data: int (4 bytes)
        data = header["NRows"]
        f.write(struct.pack('<i', data))
        data = header["NCols"]
        f.write(struct.pack('<i', data))

        # Expected binary data: float (4 bytes)
        data = header["FoVRows"]
        f.write(struct.pack('<f', data))
        data = header["FoVCols"]
        f.write(struct.pack('<f', data))
        data = header["SliceThickness"]
        f.write(struct.pack('<f', data))
        data = header["GapThickness"]
        f.write(struct.pack('<f', data))

        # Expected binary data: int (4 bytes)
        data = header["NrOfPastSpatialTransformations"]
        f.write(struct.pack('<i', data))

        if header["NrOfPastSpatialTransformations"] != 0:
            for i in range(header["NrOfPastSpatialTransformations"]):
                # Expected binary data: variable-length string
                data = header["PastTransformation"][i]["Name"]
                write_variable_length_string(f, data)

                # Expected binary data: int (4 bytes)
                data = header["PastTransformation"][i]["Type"]
                f.write(struct.pack('<i', data))

                # Expected binary data: variable-length string
                data = header["PastTransformation"][i]["SourceFileName"]
                write_variable_length_string(f, data)

                # Expected binary data: int (4 bytes)
                data = header["PastTransformation"][i]["NrOfValues"]
                f.write(struct.pack('<i', data))

                # Transformation values are stored as a list
                trans_values = header["PastTransformation"][i]["Values"]
                for j in range(header["PastTransformation"][i]["NrOfValues"]):
                    # Expected binary data: float (4 bytes)
                    f.write(struct.pack('<f', trans_values[j]))

        # Expected binary data: char (1 byte)
        data = header["LeftRightConvention"]
        f.write(struct.pack('<B', data))

        if header["File version"] >= 4:
            data = header["ReferenceSpaceVMR"]
            f.write(struct.pack('<B', data))

        # Expected binary data: float (4 bytes)
        data = header["VoxelSizeX"]
        f.write(struct.pack('<f', data))
        data = header["VoxelSizeY"]
        f.write(struct.pack('<f', data))
        data = header["VoxelSizeZ"]
        f.write(struct.pack('<f', data))

        # Expected binary data: char (1 byte)
        data = header["VoxelResolutionVerified"]
        f.write(struct.pack('<B', data))
        data = header["VoxelResolutionInTALmm"]
        f.write(struct.pack('<B', data))

        # Expected binary data: int (4 bytes)
        data = header["VMROrigV16MinValue"]
        f.write(struct.pack('<i', data))
        data = header["VMROrigV16MeanValue"]
        f.write(struct.pack('<i', data))
        data = header["VMROrigV16MaxValue"]
        f.write(struct.pack('<i', data))

    return print("VMR saved.")


def create_vmr():
    """Create BrainVoyager VMR file with default values."""
    header = dict()

    # Pre data header
    header["File version"] = 4
    header["DimX"] = 256
    header["DimY"] = 256
    header["DimZ"] = 256

    # Post data header
    header["OffsetX"] = 0
    header["OffsetY"] = 0
    header["OffsetZ"] = 0
    header["FramingCubeDim"] = 256
    header["PosInfosVerified"] = 1
    header["CoordinateSystem"] = 0
    header["Slice1CenterX"] = -87.5
    header["Slice1CenterY"] = 0
    header["Slice1CenterZ"] = 0
    header["SliceNCenterX"] = 87.5
    header["SliceNCenterY"] = 0
    header["SliceNCenterZ"] = 0
    header["RowDirX"] = 0.0
    header["RowDirY"] = 1.0
    header["RowDirZ"] = 0.0
    header["ColDirX"] = 0.0
    header["ColDirY"] = 0.0
    header["ColDirZ"] = -1.0
    header["NRows"] = 256
    header["NCols"] = 256
    header["FoVRows"] = 256.0
    header["FoVCols"] = 256.0
    header["SliceThickness"] = 1.0
    header["GapThickness"] = 0.0
    header["NrOfPastSpatialTransformations"] = 0
    header["LeftRightConvention"] = 1
    header["ReferenceSpaceVMR"] = 0
    header["VoxelSizeX"] = 1.0
    header["VoxelSizeY"] = 1.0
    header["VoxelSizeZ"] = 1.0
    header["VoxelResolutionVerified"] = 1
    header["VoxelResolutionInTALmm"] = 1
    header["VMROrigV16MinValue"] = -1
    header["VMROrigV16MeanValue"] = -1
    header["VMROrigV16MaxValue"] = -1

    # -------------------------------------------------------------------------
    # Create data
    DimX = header["DimX"]
    DimY = header["DimY"]
    DimZ = header["DimZ"]
    dims = [DimZ, DimY, DimX]
    data = np.random.random(np.prod(dims)) * 225  # 225 for BV visualization
    data = data.reshape(dims)
    data = data.astype(np.short)

    return header, data
