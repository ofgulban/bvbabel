"""Read BrainVoyager ROI file format."""

import numpy as np

# =============================================================================
def read_roi(filename):
    """Read BrainVoyager ROI file, FileVersion = 6.
    Parameters
    ----------
    filename : string
        Path to file.
    Returns
    -------
    header : dictionary
        Voxels of interest (ROI) header.
    data_roi : list of dictionaries
        A list of dictionaries. Each dictionary holds properties of a region of
        interest.
    """
    # Read non-empty lines of the input text file
    with open(filename, "r") as f:
        lines = [r for r in (line.strip() for line in f) if r]

    # ROI header
    header = dict()
    rois = [i for i in range(len(lines)) if lines[i].startswith("NrOfRects")]
    header_rows = rois[0] 
    for line in lines[0:header_rows]:
        content = line.split(":")
        content = [i.strip() for i in content]
        if content[1].isdigit():
            header[content[0]] = int(content[1])
        else:
            header[content[0]] = content[1]
            
    # ROI data (x, y, z coordinates of voxels)
    count_roi = -1
    data_roi = list()
    for r, line in enumerate(lines[header_rows:]):
        content = line.split(":")
        content = [i.strip() for i in content]

        if content[0] == "NrOfRects":
            count_roi += 1
            data_roi.append(dict())
            data_roi[count_roi]["Coordinates"] = []  # Prepare for coordinates
            data_roi[count_roi]["NrOfRects"] = content[1]

        elif content[0] == "FromSlice":
            data_roi[count_roi]["FromSlice"] = int(content[1])
            
        elif content[0] == "Left":
            data_roi[count_roi]["Left"] = int(content[1])
            
        elif content[0] == "Right":
            data_roi[count_roi]["Right"] = int(content[1])
            
        elif content[0] == "Top":
            data_roi[count_roi]["Top"] = int(content[1])
            
        elif content[0] == "Bottom":
            data_roi[count_roi]["Bottom"] = int(content[1])

        elif content[0] == "NrOfVoxels":
            data_roi[count_roi]["NrOfVoxels"] = int(content[1])

        elif content[0].split()[0].isdigit():  # Coordinate (x,y,z)
            values = content[0].split()
            values = [int(v) for v in values]
            data_roi[count_roi]["Coordinates"].append(values)

    # Convert coordinates (x, y, z) to numpy arrays [nr_voxels, 3]
    for d in data_roi:
        d["Coordinates"] = np.asarray(d["Coordinates"])

    return header, data_roi
