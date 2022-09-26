"""Read BrainVoyager POI (surface patches of interest) file format."""

import numpy as np


# =============================================================================
def read_poi(filename):
    """Read BrainVoyager POI (surface patches of interest) file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Voxels of interest (poi) header.
    data_poi : list of dictionaries
        A list of dictionaries. Each dictionary holds properties of a patch of
        interest (a set of triangular mesh surface vertices).

    """
    # Read non-empty lines of the input text file
    with open(filename, 'r') as f:
        lines = [r for r in (line.strip() for line in f) if r]

    # POI header
    header = dict()
    header_rows = 4  # NOTE: Only counting non empty rows
    for line in lines[0:header_rows]:
        content = line.split(":")
        content = [i.strip() for i in content]
        if content[1].isdigit():
            header[content[0]] = int(content[1])
        else:
            header[content[0]] = content[1]

    # POI data (x, y, z coordinates of voxels)
    count_poi = -1
    data_poi = list()
    for r, line in enumerate(lines[header_rows:]):
        content = line.split(":")
        content = [i.strip() for i in content]

        if content[0] == "NameOfPOI":
            count_poi += 1
            data_poi.append(dict())
            data_poi[count_poi]["NameOfPOI"] = content[1]
            data_poi[count_poi]["Vertices"] = []  # Prepare for coordinates

        elif content[0] == "InfoTextFile":
            data_poi[count_poi]["InfoTextFile"] = content[1]

        elif content[0] == "ColorOfPOI":
            values = content[1].split(" ")
            values = [int(v) for v in values]
            data_poi[count_poi]["ColorOfPOI"] = values

        elif content[0] == "LabelVertex":
            data_poi[count_poi]["LabelVertex"] = int(content[1])

        elif content[0] == "NrOfVertices":
            data_poi[count_poi]["NrOfVertices"] = int(content[1])

        elif content[0].split(" ")[0].isdigit():  # Coordinate
            data_poi[count_poi]["Vertices"].append(int(content[0]))

        # ---------------------------------------------------------------------
        # Post VOI data information
        elif content[0] == "NrOfPOIMTCs":
            header["NrOfPOIMTCs"] = int(content[1])

    # -------------------------------------------------------------------------
    # Vertex indices to numpy arrays [nr_voxels]
    for d in data_poi:
        d["Vertices"] = np.asarray(d["Vertices"])

    return header, data_poi


def write_poi(filename, header, data_poi):
    """Protocol to write BrainVoyager POI files.

    Parameters
    ----------
    filename : string
        Path to file.
    header : dictionary
        Voxels of interest (VOI) header.
    data_poi : list of dictionaries
        A list of dictionaries. Each dictionary holds properties of a voxels of
        interest.

    """
    with open(filename, 'w') as f:
        f.write("\n")

        data = header["FileVersion"]
        f.write("FileVersion:                   {}\n".format(data))
        f.write("\n")

        data = header["FromMeshFile"]
        f.write("FromMeshFile:                  {}\n".format(data))
        f.write("\n")

        data = header["NrOfMeshVertices"]
        f.write("NrOfMeshVertices:              {}\n".format(data))
        f.write("\n")

        data = header["NrOfPOIs"]
        f.write("NrOfPOIs:                      {}\n".format(data))
        f.write("\n\n")

        # ---------------------------------------------------------------------
        # POI data
        for v in data_poi:
            data = v["NameOfPOI"]
            f.write("NameOfPOI:  {}\n".format(data))
            data = v["InfoTextFile"]
            f.write("InfoTextFile:  {}\n".format(data))
            data = v["ColorOfPOI"]
            f.write("ColorOfPOI: {} {} {}\n".format(data[0], data[1], data[2]))
            data = v["LabelVertex"]
            f.write("LabelVertex:  {}\n".format(data))

            data = v["NrOfVertices"]
            f.write("NrOfVertices: {}\n".format(data))

            data = v["Vertices"]
            for d in data:
                f.write("{}\n".format(d))
            f.write("\n")

        # ---------------------------------------------------------------------
        # Post VOI data
        f.write("\n")
        data = header["NrOfPOIMTCs"]
        f.write("NrOfPOIMTCs: {}\n".format(data))
