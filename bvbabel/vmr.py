"""Read, write, create Brainvoyager VMR file format."""

import struct
import numpy as np


# =============================================================================
def read_vmr(filename):
    """Read Brainvoyager VMR file.

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
                            dtype="<B")
        for i in range(data_img.size):
            data_img[i], = struct.unpack('<B', f.read(1))
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
            header["X offset"] = data
            data, = struct.unpack('<h', f.read(2))
            header["Y offset"] = data
            data, = struct.unpack('<h', f.read(2))
            header["Z offset"] = data
            data, = struct.unpack('<h', f.read(2))
            header["Framing cube dimensions"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["PosInfosVerified"] = data
        data, = struct.unpack('<i', f.read(4))
        header["Coordinate system"] = data

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', f.read(4))
        header["First slice center X coordinate"] = data
        data, = struct.unpack('<f', f.read(4))
        header["First slice center Y coordinate"] = data
        data, = struct.unpack('<f', f.read(4))
        header["First slice center Z coordinate"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Last slice center X coordinate"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Last slice center Y coordinate"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Last slice center Z coordinate"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Slice row direction vector of X component"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Slice row direction vector of Y component"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Slice row direction vector of Z component"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Slice column direction vector of X component"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Slice column direction vector of Y component"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Slice column direction vector of Z component"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["Nr of rows of slice image matrix"] = data
        data, = struct.unpack('<i', f.read(4))
        header["Nr of columns of slice image matrix"] = data

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', f.read(4))
        header["Extent of field of view (FoV) in row direction [mm]"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Extent of field of view (FoV) in column direction [mm]"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Slice thickness in mm"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Gap thickness in mm"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["NrOfPastSpatialTransformations"] = data

        if header["NrOfPastSpatialTransformations"] != 0:
            # NOTE(Developer Guide 2.6): For each past transformation, the
            # information specified in the following table is stored. The
            # "type of transformation" is a value determining how many
            # subsequent values define the transformation:
            #   "1": Rigid body+scale (3 translation, 3 rotation, 3 scale)
            #   "2": Affine transformation (4x4 matrix)
            #   "4": Talairach transformation
            #   "5": Un-Talairach transformation
            pass

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', f.read(1))
        header["Left-right convention"] = data  # modified in v4
        data, = struct.unpack('<B', f.read(1))
        header["Reference space flag"] = data  # new in v4

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', f.read(4))
        header["Voxel resolution along X axis"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Voxel resolution along Y axis"] = data
        data, = struct.unpack('<f', f.read(4))
        header["Voxel resolution along Z axis"] = data

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', f.read(1))
        header["Flag for voxel resolution verified"] = data
        data, = struct.unpack('<B', f.read(1))
        header["Flag for Talairach space mm"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["Min intensity value in original 16-bit data"] = data
        data, = struct.unpack('<i', f.read(4))
        header["Mean intensity value in original 16-bit data"] = data
        data, = struct.unpack('<i', f.read(4))
        header["Max intensity value in original 16-bit data"] = data

    return header, data_img


def write_vmr(header, data_img, filename):
    """Write Brainvoyager VMR file.

    Parameters
    ----------
    header : dictionary
        Header of VMR file.
    data_img : numpy.array, 3D
        Image.
    filename : string
        Output filename.

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

        # Expected binary data: unsigned char (1 byte)
        data_img = data_img.flatten()
        for i in range(data_img.size):
            f.write(struct.pack('<B', data_img[i]))

        # ---------------------------------------------------------------------
        # VMR Post-Data Header
        # ---------------------------------------------------------------------
        if header["File version"] >= 3:
            # Expected binary data: short int (2 bytes)
            data = header["X offset"]
            f.write(struct.pack('<h', data))
            data = header["Y offset"]
            f.write(struct.pack('<h', data))
            data = header["Z offset"]
            f.write(struct.pack('<h', data))
            data = header["Framing cube dimensions"]
            f.write(struct.pack('<h', data))

        # Expected binary data: int (4 bytes)
        data = header["PosInfosVerified"]
        f.write(struct.pack('<i', data))
        data = header["Coordinate system"]
        f.write(struct.pack('<i', data))

        # Expected binary data: float (4 bytes)
        data = header["First slice center X coordinate"]
        f.write(struct.pack('<f', data))
        data = header["First slice center Y coordinate"]
        f.write(struct.pack('<f', data))
        data = header["First slice center Z coordinate"]
        f.write(struct.pack('<f', data))
        data = header["Last slice center X coordinate"]
        f.write(struct.pack('<f', data))
        data = header["Last slice center Y coordinate"]
        f.write(struct.pack('<f', data))
        data = header["Last slice center Z coordinate"]
        f.write(struct.pack('<f', data))
        data = header["Slice row direction vector of X component"]
        f.write(struct.pack('<f', data))
        data = header["Slice row direction vector of Y component"]
        f.write(struct.pack('<f', data))
        data = header["Slice row direction vector of Z component"]
        f.write(struct.pack('<f', data))
        data = header["Slice column direction vector of X component"]
        f.write(struct.pack('<f', data))
        data = header["Slice column direction vector of Y component"]
        f.write(struct.pack('<f', data))
        data = header["Slice column direction vector of Z component"]
        f.write(struct.pack('<f', data))

        # Expected binary data: int (4 bytes)
        data = header["Nr of rows of slice image matrix"]
        f.write(struct.pack('<i', data))
        data = header["Nr of columns of slice image matrix"]
        f.write(struct.pack('<i', data))

        # Expected binary data: float (4 bytes)
        data = header["Extent of field of view (FoV) in row direction [mm]"]
        f.write(struct.pack('<f', data))
        data = header["Extent of field of view (FoV) in column direction [mm]"]
        f.write(struct.pack('<f', data))
        data = header["Slice thickness in mm"]
        f.write(struct.pack('<f', data))
        data = header["Gap thickness in mm"]
        f.write(struct.pack('<f', data))

        # Expected binary data: int (4 bytes)
        data = header["NrOfPastSpatialTransformations"]
        f.write(struct.pack('<i', data))

        if header["NrOfPastSpatialTransformations"] != 0:
            pass

        # Expected binary data: char (1 byte)
        data = header["Left-right convention"]
        f.write(struct.pack('<B', data))
        data = header["Reference space flag"]
        f.write(struct.pack('<B', data))

        # Expected binary data: float (4 bytes)
        data = header["Voxel resolution along X axis"]
        f.write(struct.pack('<f', data))
        data = header["Voxel resolution along Y axis"]
        f.write(struct.pack('<f', data))
        data = header["Voxel resolution along Z axis"]
        f.write(struct.pack('<f', data))

        # Expected binary data: char (1 byte)
        data = header["Flag for voxel resolution verified"]
        f.write(struct.pack('<B', data))
        data = header["Flag for Talairach space mm"]
        f.write(struct.pack('<B', data))

        # Expected binary data: int (4 bytes)
        data = header["Min intensity value in original 16-bit data"]
        f.write(struct.pack('<i', data))
        data = header["Mean intensity value in original 16-bit data"]
        f.write(struct.pack('<i', data))
        data = header["Max intensity value in original 16-bit data"]
        f.write(struct.pack('<i', data))

    return print("VMR saved.")
