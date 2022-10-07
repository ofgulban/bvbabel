"""Read BrainVoyager PRT file format."""

from curses.ascii import isdigit
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

    # POI header
    header = dict()
    header_rows = 10  # NOTE: Only counting non empty rows
    for line in lines[0:header_rows]:
        content = line.split(":")
        content = [i.strip() for i in content]
        if content[1].isdigit():
            header[content[0]] = int(content[1])
        else:
            header[content[0]] = content[1]

    # POI data
    data_prt = list()
    count_cond = 0
    i = copy(header_rows)
    while i < len(lines):
        data_prt.append(dict())

        # Add condition name
        data_prt[count_cond]["NameOfCondition"] = lines[i]

        # Add condition occurances
        n = int(lines[i+1])
        data_prt[count_cond]["NrOfOccurances"] = n

        # Add timings
        data_prt[count_cond]["Time start"] = np.zeros(n)
        data_prt[count_cond]["Time stop"] = np.zeros(n)
        for j in range(n):
            values = lines[i+2+j].split(" ")
            data_prt[count_cond]["Time start"][j] = int(values[0])
            data_prt[count_cond]["Time stop"][j] = int(values[-1])

        # Add color
        values = lines[i+2+n].split(" ")
        data_prt[count_cond]["Color"] = list()
        for v in values:
            if v.isdigit():
                data_prt[count_cond]["Color"].append(int(v))
        data_prt[count_cond]["Color"] = np.asarray(data_prt[count_cond]["Color"])

        i += n + 3
        count_cond += 1

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
        data = header["ReferenceFuncColor"]
        f.write("ReferenceFuncColor: {}\n".format(data))
        data = header["ReferenceFuncThick"]
        f.write("ReferenceFuncThick: {}\n".format(data))
        f.write("\n")

        data = header["NrOfConditions"]
        f.write("NrOfConditions:     {}\n".format(data))
        f.write("\n")

        for i in data_prt:
            # wip
            pass
