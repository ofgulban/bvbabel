"""Read BrainVoyager VOI file format."""

import numpy as np


# =============================================================================
def read_voi(filename):
    """Read Brainvoyager VOI file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Voxels of interest (VOI) header.
    data : list of dictionaries
        A list of dictionaries. Each dictionary holds properties of a voxels of
        interest.

    """
    # Read non-empty lines of the input text file
    with open(filename, 'r') as f:
        lines = [r for r in (line.strip() for line in f) if r]

    # VOI header
    header = dict()
    header_rows = 12
    for line in lines[0:header_rows]:
        content = line.split(":")
        content = [i.strip() for i in content]
        if content[1].isdigit():
            header[content[0]] = int(content[1])
        else:
            header[content[0]] = content[1]

    # VOI data (x, y, z coordinates of voxels)
    count_voi = -1
    data = list()
    for r, line in enumerate(lines[header_rows:]):
        content = line.split(":")
        content = [i.strip() for i in content]

        if content[0] == "NameOfVOI":
            count_voi += 1
            data.append(dict())
            data[count_voi]["Coordinates"] = []  # Prepare for coordinates
            data[count_voi]["NameOfVOI"] = content[1]

        elif content[0] == "NrOfVOIVTCs":
            break

        elif content[0] == "ColorOfVOI":
            values = content[1].split(" ")
            values = [int(v) for v in values]
            data[count_voi]["ColorOfVOI"] = values

        elif content[0] == "NrOfVoxels":
            data[count_voi]["NrOfVoxels"] = int(content[1])

        else:
            values = content[0].split(" ")
            values = [int(v) for v in values]
            data[count_voi]["Coordinates"].append(values)

    # Handle VOI VTC information at the end
    header["NrOfVOIVTCs"] = int(content[1])
    header["VOIVTCs"] = []
    for line in lines[r+header_rows+1:]:
        header["VOIVTCs"].append(line)

    # Convert coordinates (x, y, z) to numpy arrays [nr_voxels, 3]
    for d in data:
        d["Coordinates"] = np.asarray(d["Coordinates"])

    return header, data
