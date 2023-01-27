"""Read BrainVoyager PRT file format."""

import numpy as np
from copy import copy


# =============================================================================
def read_prt(filename):
    """Read BrainVoyager PRT file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Protocol (PRT) header.
    data_prt : list of dictionaries
        TODO

    """
    # Read non-empty lines of the input text file
    with open(filename, 'r') as f:
        lines = [r for r in (line.strip() for line in f) if r]

    # PRT header
    header = dict()

    for j in range(0, len(lines)):
        line = lines[j]
        content = line.strip()
        content = content.split(":", 1)
        content = [i.strip() for i in content]

        if content[0].isdigit():
            pass
        elif content[0] == "FileVersion":
            header[content[0]] = content[1]
        elif content[0] == "ResolutionOfTime":
            header[content[0]] = content[1]
        elif content[0] == "Experiment":
            header[content[0]] = content[1]
        elif content[0] == "BackgroundColor":
            header[content[0]] = content[1]
        elif content[0] == "TextColor":
            header[content[0]] = content[1]
        elif content[0] == "TimeCourseColor":
            header[content[0]] = content[1]
        elif content[0] == "TimeCourseThick":
            header[content[0]] = content[1]
        elif content[0] == "ReferenceFuncColor":
            header[content[0]] = content[1]
        elif content[0] == "ReferenceFuncThick":
            header[content[0]] = content[1]

        # NOTE: The "ParametricWeights" seems to appear with "FileVersion: 3"
        elif content[0] == "ParametricWeights":
            header[content[0]] = int(content[1])

        elif content[0] == "NrOfConditions":
            header[content[0]] = content[1]
            header_rows = copy(j+1)

    # -------------------------------------------------------------------------
    # PRT data
    data_prt = list()
    count_c = 0  # Count condition
    i = copy(header_rows)
    while i < len(lines):
        data_prt.append(dict())

        # Add condition name
        data_prt[count_c]["NameOfCondition"] = lines[i]

        # Add condition occurances
        n = int(lines[i+1])
        data_prt[count_c]["NrOfOccurances"] = n

        # Add timings
        data_prt[count_c]["Time start"] = np.zeros(n, dtype=int)
        data_prt[count_c]["Time stop"] = np.zeros(n, dtype=int)
        for j in range(n):
            values = lines[i+2+j].split()
            data_prt[count_c]["Time start"][j] = int(values[0])
            data_prt[count_c]["Time stop"][j] = int(values[1])

        # Add parametric weights
        if "ParametricWeights" in header and header["ParametricWeights"] > 0:
            data_prt[count_c]["Parametric weight"] = np.zeros(n, dtype=float)
            for j in range(n):
                values = lines[i+2+j].split()
                data_prt[count_c]["Parametric weight"][j] = float(values[2])

        # Add color
        values = lines[i+2+n].split(" ")
        data_prt[count_c]["Color"] = list()
        for v in values:
            if v.isdigit():
                data_prt[count_c]["Color"].append(int(v))
        data_prt[count_c]["Color"] = np.asarray(data_prt[count_c]["Color"])

        i += n + 3
        count_c += 1

    return header, data_prt


# =============================================================================
def write_prt(filename, header, data_prt):
    """Protocol to write BrainVoyager PRT file.

    Parameters
    ----------
    filename : string
        Path to file.
    header : dictionary
        Protocol (PRT) header.
    data_prt : list of dictionaries
        TODO

    """
    with open(filename, 'w') as f:
        f.write("\n")

        data = header["FileVersion"]
        f.write("FileVersion:        {}\n".format(data))
        f.write("\n")

        data = header["ResolutionOfTime"]
        f.write("ResolutionOfTime:   {}\n".format(data))
        f.write("\n")

        data = header["Experiment"]
        f.write("Experiment:         {}\n".format(data))
        f.write("\n")

        data = header["BackgroundColor"]
        f.write("BackgroundColor:    {}\n".format(data))
        data = header["TextColor"]
        f.write("TextColor:          {}\n".format(data))
        data = header["TimeCourseColor"]
        f.write("TimeCourseColor:    {}\n".format(data))
        data = header["TimeCourseThick"]
        f.write("TimeCourseThick:    {}\n".format(data))
        data = header["ReferenceFuncColor"]
        f.write("ReferenceFuncColor: {}\n".format(data))
        data = header["ReferenceFuncThick"]
        f.write("ReferenceFuncThick: {}\n".format(data))
        f.write("\n")

        if "ParametricWeights" in header:
            data = header["ParametricWeights"]
            f.write("ParametricWeights: {}\n".format(data))
            f.write("\n")

        data = header["NrOfConditions"]
        f.write("NrOfConditions: {}\n".format(data))

        for i in range(len(data_prt)):
            f.write("\n")
            data = data_prt[i]["NameOfCondition"]
            f.write("{}\n".format(data))
            data = data_prt[i]["NrOfOccurances"]
            f.write("{}\n".format(data))

            for j in range(data_prt[i]["NrOfOccurances"]):
                value1 = data_prt[i]["Time start"][j]
                value2 = data_prt[i]["Time stop"][j]
                if header["ResolutionOfTime"].lower() == "volumes":
                    value1 = int(value1)
                    value2 = int(value2)

                if "ParametricWeights" in header and header["ParametricWeights"] > 0:
                    value3 = data_prt[i]["Parametric weight"][j]
                    f.write(f"{value1:>4} {value2:>4} {value3}\n")
                else:
                    f.write(f"{value1:>4} {value2:>4}\n")

            data = data_prt[i]["Color"]
            f.write("Color: {} {} {}\n".format(data[0], data[1], data[2]))
