"""Read, write, create BrainVoyager DMR file format."""

import os
import numpy as np
from bvbabel.dwi import read_dwi
from pprint import pprint

# =============================================================================
def read_dmr(filename, rearrange_data_axes=True):
    """Read BrainVoyager DMR (and the paired DWI) file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Pre-data and post-data headers.
    data : 4D numpy.array, (x, y, slices, directions)
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
    header = dict()
    info_pos = dict()
    info_tra = dict()
    info_grad = dict()
    info_multiband = dict()

    with open(filename, 'r') as f:
        lines = f.readlines()
        for j in range(0, len(lines)):
            line = lines[j]
            content = line.strip()
            content = content.split(":", 1)
            content = [i.strip() for i in content]

            # -----------------------------------------------------------------
            # NOTE[Faruk]: Quickly skip entries starting with number. This is
            # because such entries belong to other structures and are dealth
            # with below in transformations and multiband sections
            if content[0].isdigit():
                pass
            elif content[0] == "FileVersion":
                header[content[0]] = content[1]
            elif content[0] == "NrOfVolumes": # is number of directions
                header[content[0]] = int(content[1])
            elif content[0] == "NrOfSlices":
                header[content[0]] = int(content[1])
            elif content[0] == "NrOfSkippedVolumes":
                header[content[0]] = content[1]
            elif content[0] == "Prefix":
                header[content[0]] = content[1].strip("\"")
            elif content[0] == "DataStorageFormat":
                header[content[0]] = int(content[1])
            elif content[0] == "DataType":
                header[content[0]] = int(content[1])
            elif content[0] == "TR":
                header[content[0]] = content[1]
            elif content[0] == "InterSliceTime":
                header[content[0]] = content[1]
            elif content[0] == "TimeResolutionVerified":
                header[content[0]] = content[1]
            elif content[0] == "TE":
                header[content[0]] = content[1]
            elif content[0] == "SliceAcquisitionOrder":
                header[content[0]] = content[1]
            elif content[0] == "SliceAcquisitionOrderVerified":
                header[content[0]] = content[1]
            elif content[0] == "ResolutionX":
                header[content[0]] = int(content[1])
            elif content[0] == "NrOfColumns":
                content[0] = "ResolutionX"
                header[content[0]] = int(content[1])
            elif content[0] == "ResolutionY":
                header[content[0]] = int(content[1])
            elif content[0] == "NrOfRows":
                content[0] = "ResolutionY"
                header[content[0]] = int(content[1])
            elif content[0] == "LoadAMRFile":
                header[content[0]] = content[1].strip("\"")
            elif content[0] == "ShowAMRFile":
                header[content[0]] = content[1]
            elif content[0] == "ImageIndex":
                header[content[0]] = content[1]
            elif content[0] == "LayoutNColumns":
                header[content[0]] = content[1]
            elif content[0] == "LayoutNRows":
                header[content[0]] = content[1]
            elif content[0] == "LayoutZoomLevel":
                header[content[0]] = content[1]
            elif content[0] == "SegmentSize":
                header[content[0]] = content[1]
            elif content[0] == "SegmentOffset":
                header[content[0]] = content[1]
            elif content[0] == "DisplayVolume": #
                header[content[0]] = content[1]
            elif content[0] == "NrOfLinkedProtocols":
                header[content[0]] = content[1]
            elif content[0] == "ProtocolFile":
                header[content[0]] = content[1].strip("\"")
            elif content[0] == "InplaneResolutionX":
                header[content[0]] = content[1]
            elif content[0] == "InplaneResolutionY":
                header[content[0]] = content[1]
            elif content[0] == "SliceThickness":
                header[content[0]] = content[1]
                # NOTE[Faruk]: This is duplicate entry that appears in position
                # information header too. I decided to use the last occurance
                # as the true value for both header entries. These two entries
                # should always match if the source file is not manipulated in
                # some way.
                info_pos[content[0]] = content[1]
            elif content[0] == "SliceGap":
                header[content[0]] = content[1]
            elif content[0] == "VoxelResolutionVerified":
                header[content[0]] = content[1]

            # -----------------------------------------------------------------
            # Position information
            elif content[0] == "PositionInformationFromImageHeaders":
                pass  # No info to be stored here
            elif content[0] == "PosInfosVerified":
                info_pos[content[0]] = content[1]
            elif content[0] == "CoordinateSystem":
                info_pos[content[0]] = content[1]
            elif content[0] == "Slice1CenterX":
                info_pos[content[0]] = content[1]
            elif content[0] == "Slice1CenterY":
                info_pos[content[0]] = content[1]
            elif content[0] == "Slice1CenterZ":
                info_pos[content[0]] = content[1]
            elif content[0] == "SliceNCenterX":
                info_pos[content[0]] = content[1]
            elif content[0] == "SliceNCenterY":
                info_pos[content[0]] = content[1]
            elif content[0] == "SliceNCenterZ":
                info_pos[content[0]] = content[1]
            elif content[0] == "RowDirX":
                info_pos[content[0]] = content[1]
            elif content[0] == "RowDirY":
                info_pos[content[0]] = content[1]
            elif content[0] == "RowDirZ":
                info_pos[content[0]] = content[1]
            elif content[0] == "ColDirX":
                info_pos[content[0]] = content[1]
            elif content[0] == "ColDirY":
                info_pos[content[0]] = content[1]
            elif content[0] == "ColDirZ":
                info_pos[content[0]] = content[1]
            elif content[0] == "NRows":
                info_pos[content[0]] = content[1]
            elif content[0] == "NCols":
                info_pos[content[0]] = content[1]
            elif content[0] == "FoVRows":
                info_pos[content[0]] = content[1]
            elif content[0] == "FoVCols":
                info_pos[content[0]] = content[1]
            elif content[0] == "SliceThickness":
                # NOTE[Faruk]: This is duplicate entry that appears twice.
                # See header['SliceThickness'] section above.
                pass
            elif content[0] == "GapThickness":
                info_pos[content[0]] = content[1]

            # -----------------------------------------------------------------
            # Transformations section
            elif content[0] == "NrOfPastSpatialTransformations":
                info_tra[content[0]] = int(content[1])
            elif content[0] == "NameOfSpatialTransformation":
                info_tra[content[0]] = content[1]
            elif content[0] == "TypeOfSpatialTransformation":
                info_tra[content[0]] = content[1]
            elif content[0] == "AppliedToFileName":
                info_tra[content[0]] = content[1]
            elif content[0] == "NrOfTransformationValues":
                info_tra[content[0]] = content[1]

                # NOTE(Faruk): I dont like this matrix reader but I don't see a
                # more elegant way for now.
                nr_values = int(content[1])
                affine = []
                v = 0  # Counter for values
                n = 1  # Counter for lines
                while v < nr_values:
                    line = lines[j + n]
                    content = line.strip()
                    content = content.split()
                    for val in content:
                        affine.append(float(val))
                    v += len(content)  # Count values
                    n += 1  # Iterate line
                affine = np.reshape(np.asarray(affine), (4, 4))
                info_tra["Transformation matrix"] = affine
            # -----------------------------------------------------------------
            # Gradients
            elif content[0] == "GradientDirectionsVerified":
                info_grad[content[0]] = content[1]
            elif content[0] == "GradientXDirInterpretation":
                info_grad[content[0]] = content[1]
            elif content[0] == "GradientYDirInterpretation":
                info_grad[content[0]] = content[1]
            elif content[0] == "GradientZDirInterpretation":
                info_grad[content[0]] = content[1]
            elif content[0] == "GradientInformationAvailable":
                info_grad[content[0]] = content[1]
                if info_grad["GradientInformationAvailable"] == "YES":
                    graddirs = []
                    for k in range(1, header["NrOfVolumes"]+1):
                        line = lines[j + k]
                        content = line.strip()
                        content = content.split()
                        for val in content:
                            graddirs.append(float(val))
                    graddirs = np.reshape(np.asarray(graddirs), (4, header["NrOfVolumes"]))
                    info_grad["Gradients"] = graddirs
                
            # -----------------------------------------------------------------
            # This part only contains a single information
            elif content[0] == "LeftRightConvention":
                header[content[0]] = content[1]

            # -----------------------------------------------------------------
            # Multiband section
            elif content[0] == "FirstDataSourceFile":
                info_multiband[content[0]] = content[1]
            elif content[0] == "MultibandSequence":
                info_multiband[content[0]] = content[1]
            elif content[0] == "MultibandFactor":
                info_multiband[content[0]] = content[1]
            elif content[0] == "SliceTimingTableSize":
                info_multiband[content[0]] = int(content[1])

                # NOTE(Faruk): I dont like this matrix reader but I don't see a
                # more elegant way for now.
                nr_values = int(content[1])
                slice_timings = []
                for n in range(1, nr_values+1):
                    line = lines[j + n]
                    content = line.strip()
                    slice_timings.append(float(content))
                info_multiband["Slice timings"] = slice_timings

            elif content[0] == "AcqusitionTime":
                info_multiband[content[0]] = content[1]
    header["Position information"] = info_pos
    header["Transformation information"] = info_tra
    header["Gradient information"] = info_grad
    header["Multiband information"] = info_multiband

    # -------------------------------------------------------------------------
    # Access data from the separate DWI file
    dirname = os.path.dirname(filename)
    filename_dwi = os.path.join(dirname, "{}.dwi".format(header["Prefix"]))

    data_img = read_dwi(filename_dwi, nr_slices=header["NrOfSlices"],
                        nr_directions=header["NrOfVolumes"],
                        res_x=header["ResolutionX"],
                        res_y=header["ResolutionY"],
                        data_type=header["DataType"],
                        rearrange_data_axes=rearrange_data_axes)
    
    return header, data_img


##FILE = "human31dir_bv214.dmr" # "case1_3_1_default.dmr"
##header, data = read_dmr(FILE)
##pprint(header)
