"""Read BrainVoyager SDM file format."""

import numpy as np


# =============================================================================
def read_sdm(filename):
    """Read BrainVoyager SDM file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Single subjects design matrix (SDM) header. Also used for storing
        motion estimates (*_3DMC.sdm).
    data : list
        Each element contains a dictionary that contains the information of
        a single predictor.

    Description
    -------
    An SDM file consists of the following header fields: 'FileVersion',
    'NrOfPredictors', 'NrOfDataPoints', 'IncludesConstant',
    'FirstConfoundPredictor'. Data are columns: NrOfDataPoints x NrOfPredictors
    weights (float); each predictor/regressor column is preceded by a triple of
    RGB color values, each between 0-255, saved as header["Colors"], and names,
    saved as header["PredictorNames"].

    """
    # Read non-empty lines of the input text file
    with open(filename, 'r') as f:
        lines = [r for r in (line.strip() for line in f) if r]

    # SDM header
    header = dict()
    header_rows = 5  # Nr of rows without empty lines
    for line in lines[0:header_rows]:
        content = line.split(":")
        content = [i.strip() for i in content]
        if content[1].isdigit():
            header[content[0]] = int(content[1])
        else:
            header[content[0]] = content[1]

    # -----------------------------------------------------------------------------
    # SDM data columnns
    nr_cols = header["NrOfPredictors"]
    nr_rows = header["NrOfDataPoints"]

    # Parse column colors (RGB integer triplets for each column)
    col_rgb_row = 5
    colors = [i for i in lines[col_rgb_row].split(" ") if i.isdigit()]
    col_rgb = list()
    for i in range(0, nr_cols*3, 3):
        col_rgb.append([int(colors[i]), int(colors[i+1]), int(colors[i+2])])

    # Parse column names
    col_name_row = 6
    col_name = [i.strip("\"") for i in lines[col_name_row].split("\" \"") if i]

    # Parse column data
    col_values_row = 7
    col_values = np.zeros((nr_rows, nr_cols))
    for r, line in enumerate(lines[col_values_row:]):
        temp = line.replace("e-", "!@#$%")  # Preserve scientific notation
        temp = temp.replace("-", " -")  # Separate concatenated columns
        temp = temp.replace("!@#$%", "e-")  # Restore scientific notation
        temp = temp.split(" ")
        col_values[r, :] = [float(i.strip()) for i in temp if i]

    # -----------------------------------------------------------------------------
    # Reorganize column information
    data = list()
    for i in range(nr_cols):
        temp = dict()
        temp["NameOfPredictor"] = col_name[i]
        temp["ColorOfPredictor"] = col_rgb[i]
        temp["ValuesOfPredictor"] = col_values[:, i]
        data.append(temp)

    return header, data


def write_sdm(filename, header, data_sdm):
    """Protocol to write BrainVoyager SDM file.

    Parameters
    ----------
    filename : string
        Path to file.
    header : dictionary
        Single subjects design matrix (SDM) header. Also used for storing
        motion estimates (*_3DMC.sdm).
    data_sdm : list
        Each element contains a dictionary that contains the information of
        a single predictor.

    """
    with open(filename, 'w') as f:
        data = header["FileVersion"]
        f.write("FileVersion:                   {}\n".format(data))
        f.write("\n")

        data = header["NrOfPredictors"]
        f.write("NrOfPredictors:                {}\n".format(data))
        data = header["NrOfDataPoints"]
        f.write("NrOfDataPoints:                {}\n".format(data))
        data = header["IncludesConstant"]
        f.write("IncludesConstant:              {}\n".format(data))
        data = header["FirstConfoundPredictor"]
        f.write("FirstConfoundPredictor:        {}\n".format(data))
        f.write("\n")

        # ---------------------------------------------------------------------
        # Write column colors
        nr_cols = header["NrOfPredictors"]
        for i in range(nr_cols):
            f.write("{} {} {}".format(data_sdm[i]["ColorOfPredictor"][0],
                                      data_sdm[i]["ColorOfPredictor"][1],
                                      data_sdm[i]["ColorOfPredictor"][2]))
            if i < nr_cols-1:
                f.write("   ")
            else:
                f.write("\n")

        # ---------------------------------------------------------------------
        # Write column names
        for i in range(nr_cols):
            f.write("\"{}\"".format(data_sdm[i]["NameOfPredictor"]))
            if i < nr_cols-1:
                f.write(" ")
            else:
                f.write("\n")

        # ---------------------------------------------------------------------
        # Write column values
        nr_rows = header["NrOfDataPoints"]
        for i in range(nr_rows):
            for j in range(nr_cols):
                value = data_sdm[j]["ValuesOfPredictor"][i]
                f.write("{:.9f}".format(value).rjust(12))
                if j < nr_cols-1:
                    f.write(" ")
                else:
                    f.write("\n")
