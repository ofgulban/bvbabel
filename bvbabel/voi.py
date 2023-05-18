"""Read BrainVoyager VOI file format."""

import numpy as np


# =============================================================================
def read_voi(filename):
    """Read BrainVoyager VOI file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Voxels of interest (VOI) header.
    data_voi : list of dictionaries
        A list of dictionaries. Each dictionary holds properties of a voxels of
        interest.

    """
    # Read non-empty lines of the input text file
    with open(filename, 'r') as f:
        lines = [r for r in (line.strip() for line in f) if r]

    # VOI header
    header = dict()
    header_rows = 12  # NOTE: Only counting non empty rows
    for line in lines[0:header_rows]:
        content = line.split(":")
        content = [i.strip() for i in content]
        if content[1].isdigit():
            header[content[0]] = int(content[1])
        else:
            header[content[0]] = content[1]

    # VOI data (x, y, z coordinates of voxels)
    count_voi = -1
    data_voi = list()
    for r, line in enumerate(lines[header_rows:]):
        content = line.split(":")
        content = [i.strip() for i in content]

        if content[0] == "NameOfVOI":
            count_voi += 1
            data_voi.append(dict())
            data_voi[count_voi]["Coordinates"] = []  # Prepare for coordinates
            data_voi[count_voi]["NameOfVOI"] = content[1]

        elif content[0] == "ColorOfVOI":
            values = content[1].split(" ")
            values = [int(v) for v in values]
            data_voi[count_voi]["ColorOfVOI"] = values

        elif content[0] == "NrOfVoxels":
            data_voi[count_voi]["NrOfVoxels"] = int(content[1])

        elif content[0].strip("-").split(" ")[0].isdigit():  # Coordinate
            values = content[0].split(" ")
            values = [int(v) for v in values]
            data_voi[count_voi]["Coordinates"].append(values)

        # ---------------------------------------------------------------------
        # Post VOI data information
        elif content[0] == "NrOfVOIVTCs":
            header["NrOfVOIVTCs"] = int(content[1])

        elif len(content) > 1 and len(content) < 3:  # A path containing ':'
            header["VOIVTCs"] = "{}:{}".format(content[0], content[1])

        else:  # File path that does not contain ':'
            header["VOIVTCs"] = content[0]

        # ---------------------------------------------------------------------
        # else:
        #     values = content[0].split(" ")
        #     values = [int(v) for v in values]
        #     data_voi[count_voi]["Coordinates"].append(values)

    # Convert coordinates (x, y, z) to numpy arrays [nr_voxels, 3]
    for d in data_voi:
        d["Coordinates"] = np.asarray(d["Coordinates"])

    return header, data_voi


def write_voi(filename, header, data_voi):
    """Protocol to write BrainVoyager VOI file.

    Parameters
    ----------
    filename : string
        Path to file.
    header : dictionary
        Voxels of interest (VOI) header.
    data_voi : list of dictionaries
        A list of dictionaries. Each dictionary holds properties of a voxels of
        interest.

    """
    with open(filename, 'w') as f:
        f.write("\n")

        data = header["FileVersion"]
        f.write("FileVersion:                   {}\n".format(data))
        f.write("\n")

        data = header["ReferenceSpace"]
        f.write("ReferenceSpace:                {}\n".format(data))
        f.write("\n")

        data = header["OriginalVMRResolutionX"]
        f.write("OriginalVMRResolutionX:        {}\n".format(data))
        data = header["OriginalVMRResolutionY"]
        f.write("OriginalVMRResolutionY:        {}\n".format(data))
        data = header["OriginalVMRResolutionZ"]
        f.write("OriginalVMRResolutionZ:        {}\n".format(data))
        data = header["OriginalVMROffsetX"]
        f.write("OriginalVMROffsetX:            {}\n".format(data))
        data = header["OriginalVMROffsetY"]
        f.write("OriginalVMROffsetY:            {}\n".format(data))
        data = header["OriginalVMROffsetZ"]
        f.write("OriginalVMROffsetZ:            {}\n".format(data))
        data = header["OriginalVMRFramingCubeDim"]
        f.write("OriginalVMRFramingCubeDim:     {}\n".format(data))
        f.write("\n")

        data = header["LeftRightConvention"]
        f.write("LeftRightConvention:           {}\n".format(data))
        f.write("\n")

        data = header["SubjectVOINamingConvention"]
        f.write("SubjectVOINamingConvention:    {}\n".format(data))
        f.write("\n\n")

        data = header["NrOfVOIs"]
        f.write("NrOfVOIs:                      {}\n".format(data))
        f.write("\n")

        # ---------------------------------------------------------------------
        # VOI data
        for v in data_voi:
            data = v["NameOfVOI"]
            f.write("NameOfVOI:  {}\n".format(data))
            data = v["ColorOfVOI"]
            f.write("ColorOfVOI: {} {} {}\n".format(data[0], data[1], data[2]))
            f.write("\n")

            data = v["NrOfVoxels"]
            f.write("NrOfVoxels: {}\n".format(data))

            data = v["Coordinates"]
            for d in data:
                f.write("{} {} {}\n".format(d[0], d[1], d[2]))
            f.write("\n")

        # ---------------------------------------------------------------------
        # Post VOI data
        f.write("\n")
        data = header["NrOfVOIVTCs"]
        f.write("NrOfVOIVTCs: {}\n".format(data))
        data = header["VOIVTCs"]
        f.write("{}".format(data))
