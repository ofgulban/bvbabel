"""Read BrainVoyager PRT file format."""

import numpy as np


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
    count_cond = -1
    row_cond_name = -1
    data_prt = list()
    for r, line in enumerate(lines[header_rows:]):
        content = line.split(":")
        content = [i.strip() for i in content]

        if content[0].isdigit() is False:
            count_cond += 1
            row_cond_name = r
            data_prt.append(dict())
            data_prt[count_cond]["NameOfCondition"] = content[0]
            data_prt[count_cond]["NrOfOccurances"] = None
            data_prt[count_cond]["Timings"] = []

        elif r == row_cond_name+1:
            data_prt[count_cond]["NrOfOccurances"] = int(content[0])

        elif r < row_cond_name+data_prt[count_cond]("NrOfOccurances"):
            values = content[0].split(" ")
            values = [int(v) for v in values]
            data_prt[count_cond]["Timings"].append(values)

        elif content[0] == "Color":
            values = content[1].split(" ")
            values = [int(v) for v in values]
            data_prt[count_cond]["Color"] = values

    return header, data_prt
