"""Read BrainVoyager FMR file format."""

import time
import os
import numpy as np
import nibabel as nb

FILE = "/home/faruk/Documents/test_bvbabel/fmr/nifti_converted.fmr"
OUT_NII = "/home/faruk/Documents/test_bvbabel/fmr/nifti_converted_bvbabel.nii.gz"

# =============================================================================
start = time.time()
info_fmr = dict()
info_pos = dict()
info_tra = dict()
info_multiband = dict()

# header_type = 0
with open(FILE, 'r') as f:
    lines = f.readlines()
    for j in range(0, len(lines)):
        line = lines[j]
        content = line.strip()
        content = content.split(":", 1)
        content = [i.strip() for i in content]

        # ---------------------------------------------------------------------
        # NOTE[Faruk]: Quickly skip entries starting with number. This is
        # because such entries belong to other structures and are dealth with
        # below in transformations and multiband sections
        if content[0].isdigit():
            pass
        # TODO[Faruk]: I can use each assignment for conversions from strings
        elif content[0] == "FileVersion":
            info_fmr[content[0]] = content[1]
        elif content[0] == "NrOfVolumes":
            info_fmr[content[0]] = int(content[1])
        elif content[0] == "NrOfSlices":
            info_fmr[content[0]] = int(content[1])
        elif content[0] == "NrOfSkippedVolumes":
            info_fmr[content[0]] = content[1]
        elif content[0] == "Prefix":
            info_fmr[content[0]] = content[1].strip("\"")
        elif content[0] == "DataStorageFormat":
            info_fmr[content[0]] = int(content[1])
        elif content[0] == "DataType":
            info_fmr[content[0]] = content[1]
        elif content[0] == "TR":
            info_fmr[content[0]] = content[1]
        elif content[0] == "InterSliceTime":
            info_fmr[content[0]] = content[1]
        elif content[0] == "TimeResolutionVerified":
            info_fmr[content[0]] = content[1]
        elif content[0] == "TE":
            info_fmr[content[0]] = content[1]
        elif content[0] == "SliceAcquisitionOrder":
            info_fmr[content[0]] = content[1]
        elif content[0] == "SliceAcquisitionOrderVerified":
            info_fmr[content[0]] = content[1]
        elif content[0] == "ResolutionX":
            info_fmr[content[0]] = int(content[1])
        elif content[0] == "ResolutionY":
            info_fmr[content[0]] = int(content[1])
        elif content[0] == "LoadAMRFile":
            info_fmr[content[0]] = content[1]
            info_fmr[content[0]] = content[1]
        elif content[0] == "ShowAMRFile":
            info_fmr[content[0]] = content[1]
        elif content[0] == "ImageIndex":
            info_fmr[content[0]] = content[1]
        elif content[0] == "LayoutNColumns":
            info_fmr[content[0]] = content[1]
        elif content[0] == "LayoutNRows":
            info_fmr[content[0]] = content[1]
        elif content[0] == "LayoutZoomLevel":
            info_fmr[content[0]] = content[1]
        elif content[0] == "SegmentSize":
            info_fmr[content[0]] = content[1]
        elif content[0] == "SegmentOffset":
            info_fmr[content[0]] = content[1]
        elif content[0] == "NrOfLinkedProtocols":
            info_fmr[content[0]] = content[1]
        elif content[0] == "ProtocolFile":
            info_fmr[content[0]] = content[1]
        elif content[0] == "InplaneResolutionX":
            info_fmr[content[0]] = content[1]
        elif content[0] == "InplaneResolutionY":
            info_fmr[content[0]] = content[1]
        elif content[0] == "SliceThickness":
            info_fmr[content[0]] = content[1]
        elif content[0] == "SliceGap":
            info_fmr[content[0]] = content[1]
        elif content[0] == "VoxelResolutionVerified":
            info_fmr[content[0]] = content[1]

        # ---------------------------------------------------------------------
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
            info_pos[content[0]] = content[1]
        elif content[0] == "GapThickness":
            info_pos[content[0]] = content[1]

        # ---------------------------------------------------------------------
        # Transformations section
        elif content[0] == "NrOfPastSpatialTransformations":
            info_tra[content[0]] = content[1]
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

        # ---------------------------------------------------------------------
        # This part only contains a single information
        elif content[0] == "LeftRightConvention":
            info_fmr[content[0]] = content[1]

        # ---------------------------------------------------------------------
        # Multiband section
        elif content[0] == "FirstDataSourceFile":
            info_multiband[content[0]] = content[1]
        elif content[0] == "MultibandSequence":
            info_multiband[content[0]] = content[1]
        elif content[0] == "MultibandFactor":
            info_multiband[content[0]] = content[1]
        elif content[0] == "SliceTimingTableSize":
            info_multiband[content[0]] = content[1]

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


# =============================================================================
def read_stc(filename, nr_slices, nr_volumes, res_x, res_y, data_format=2):
    """Read Brainvoyager STC file.

    Parameters
    ----------
    filename : string
        Path to file.
    nr_slices: integer
        Number of slices in each measurement. Referred to as "NrOfSlices"
        within the FMR text file.
    nr_volumes: integer
        Number of measurements (also called volumes or TRs). Referred to as
        "NrOfVolumes" within the FMR text file.
    res_x: integer
        Number of voxels along each row in each slice. Referred to as
        "ResolutionX" within the FMR text file.
    res_y: integer
        Number of voxels along each column in each slice. Referred to as
        "ResolutionY" within the FMR text file.
    data_format: integer, 1 or 2
        Each data element (intensity value) is represented either in 2 bytes
        (unsigned short) or in 4 bytes (float, default) as determined by the
        "DataStorageFormat" entry in the FMR file.

    Returns
    -------
    data : 3D numpy.array
        Image data.

    """
    if data_format == 1:
        data_img = np.fromfile(filename_stc, dtype="<H", count=-1, sep="",
                               offset=0)
    elif data_format == 2:
        data_img = np.fromfile(filename_stc, dtype="<f", count=-1, sep="",
                               offset=0)

    data_img = np.reshape(data_img, (nr_slices, nr_volumes, res_x, res_y))
    data_img = np.transpose(data_img, (3, 2, 0, 1))
    data_img = data_img[:, ::-1, ::, :]  # Flip BV axes

    return data_img


# Read STC data
dirname = os.path.dirname(FILE)
filename_stc = os.path.join(dirname, "{}.stc".format(info_fmr["Prefix"]))

data_img = read_stc(filename_stc, nr_slices=info_fmr["NrOfSlices"],
                    nr_volumes=info_fmr["NrOfVolumes"],
                    res_x=info_fmr["ResolutionX"],
                    res_y=info_fmr["ResolutionY"],
                    data_format=info_fmr["DataStorageFormat"])

# =============================================================================
# # Print header information
# print("\nFMR information")
# for key, value in info_fmr.items():
#     print("  ", key, ":", value)
#
# print("\nPosition information")
# for key, value in info_pos.items():
#     print("  ", key, ":", value)
#
# print("\nTransformation information")
# for key, value in info_tra.items():
#     print("  ", key, ":", value)
#
# print("\nMultiband information")
# for key, value in info_multiband.items():
#     print("  ", key, ":", value)

end = time.time()
print("  FMR and STC read in: {:.2f} seconds".format(end - start))

# =============================================================================
start = time.time()

# Save nifti for testing
basename = FILE.split(os.extsep, 1)[0]
outname = "{}_bvbabel.nii.gz".format(basename)
# img = nb.Nifti1Image(data_img, affine=np.eye(4))
img = nb.Nifti1Image(data_img, affine=info_tra["Transformation matrix"])
nb.save(img, outname)

end = time.time()
print("  Nifti saved in: {:.2f} seconds".format(end - start))

print("  Data dimensions: {} {} {} {}".format(info_fmr["ResolutionX"],
      info_fmr["ResolutionY"], info_fmr["NrOfSlices"], info_fmr["NrOfVolumes"])
      )

print("Finished.")
