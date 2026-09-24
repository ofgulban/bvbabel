"""
Read and write BrainVoyager ROI file format.

A BrainVoyager ROI file can contain one or more regions of interest (ROIs).
Each ROI consists of a list of voxels defining the actual region of interest
and one or more rectangles defining how the region is visualized in
BrainVoyager.

The voxel coordinates determine which voxels belong to the ROI. The rectangle
definitions are visualization information and may extend beyond the voxels 
that are actually included in the ROI.

Each rectangle is defined for a specific slice ("FromSlice"). Its boundaries
within that slice are specified by "Left", "Right", "Top", and "Bottom.
An ROI may contain multiple rectangles, including multiple rectangles on the
same slice.
"""

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
        Regions of interest (ROI) header.
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

    # ROI data (rectangle definitions and x, y, z coordinates of voxels)
    count_roi = -1
    data_roi = list()
    current_rect = None

    for line in lines[header_rows:]:
        content = line.split(":")
        content = [i.strip() for i in content]

        if content[0] == "NrOfRects":
            count_roi += 1
            data_roi.append(dict())
            data_roi[count_roi]["NrOfRects"] = int(content[1])
            data_roi[count_roi]["Rectangles"] = []
            data_roi[count_roi]["Coordinates"] = []

        elif content[0] == "FromSlice":
            current_rect = {"FromSlice": int(content[1])}
            data_roi[count_roi]["Rectangles"].append(current_rect)

        elif content[0] in ("Left", "Right", "Top", "Bottom"):
            current_rect[content[0]] = int(content[1])

        elif content[0] == "NrOfVoxels":
            data_roi[count_roi]["NrOfVoxels"] = int(content[1])

        elif content[0].split()[0].isdigit():  # Coordinate (x, y, z)
            values = content[0].split()
            values = [int(v) for v in values]
            data_roi[count_roi]["Coordinates"].append(values)

    # Convert coordinates (x, y, z) to numpy arrays [nr_voxels, 3]
    for d in data_roi:
        d["Coordinates"] = np.asarray(d["Coordinates"])

    return header, data_roi


def write_roi(filename, header, data_roi):
    """Write BrainVoyager ROI file, FileVersion = 6.

    Parameters
    ----------
    filename : string
        Path to file.
    header : dictionary
        Regions of interest (ROI) header.
    data_roi : list of dictionaries
        A list of dictionaries. Each dictionary holds properties of a region of
        interest.
    """
    with open(filename, "w") as f:
        # ROI header
        for key, data in header.items():
            f.write("{:<18}{}\n".format(key + ":", data))
            f.write("\n")

        # ---------------------------------------------------------------------
        # ROI data
        for r in data_roi:
            rectangles = r["Rectangles"]
            if int(r["NrOfRects"]) != len(rectangles):
                raise ValueError(
                    "NrOfRects ({}) does not match the number of rectangle "
                    "definitions ({})".format(r["NrOfRects"], len(rectangles))
                )

            f.write("{:<18}{}\n".format("NrOfRects:", r["NrOfRects"]))

            for rect in rectangles:
                for key in ("FromSlice", "Left", "Right", "Top", "Bottom"):
                    f.write("{:<18}{}\n".format(key + ":", rect[key]))

            coordinates = r["Coordinates"]
            if r["NrOfVoxels"] != len(coordinates):
                raise ValueError(
                    "NrOfVoxels ({}) does not match the number of coordinates "
                    "({})".format(r["NrOfVoxels"], len(coordinates))
                )

            f.write("{:<18}{}\n".format("NrOfVoxels:", r["NrOfVoxels"]))

            for d in coordinates:
                if any(int(v) < 0 for v in d):
                    raise ValueError("ROI coordinates must be non-negative integers")
                f.write("{:3d} {:3d} {:3d}\n".format(
                    int(d[0]), int(d[1]), int(d[2])
                ))
            f.write("\n")
