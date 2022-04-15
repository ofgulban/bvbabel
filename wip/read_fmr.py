"""Read BrainVoyager FMR file format."""

FILE = "/home/faruk/Documents/test_bvbabel/fmr/nifti_converted.fmr"
OUT_NII = "/home/faruk/Documents/test_bvbabel/fmr/nifti_converted_bvbabel.nii.gz"

# =============================================================================
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
            info_fmr[content[0]] = content[1]
        elif content[0] == "NrOfSlices":
            info_fmr[content[0]] = content[1]
        elif content[0] == "NrOfSkippedVolumes":
            info_fmr[content[0]] = content[1]
        elif content[0] == "Prefix":
            # info_fmr[content[0]] = content[1]  # May not need
            info_fmr[content[0]] = content[1]
        elif content[0] == "DataStorageFormat":
            info_fmr[content[0]] = content[1]
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
            info_fmr[content[0]] = content[1]
        elif content[0] == "ResolutionY":
            info_fmr[content[0]] = content[1]
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
# Print header information
print("\nFMR information")
for key, value in info_fmr.items():
    print("  ", key, ":", value)

print("\nPosition information")
for key, value in info_pos.items():
    print("  ", key, ":", value)

print("\nTransformation information")
for key, value in info_tra.items():
    print("  ", key, ":", value)

print("\nMultiband information")
for key, value in info_multiband.items():
    print("  ", key, ":", value)

# Test output data
# img_nii = nb.Nifti1Image(data, affine=np.eye(4))
# nb.save(img_nii, OUT_NII)
