"""Read BrainVoyager SDM file format."""

import numpy as np


# =============================================================================
def read_sdm(filename):
    """Read Brainvoyager SDM file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Single subjects design matrix (SDM) header. Also used for storing
        motion estimates (*_3DMC.sdm).
    data : list of dictionaries
        One dictionary containing NrOfPredictors x NrOfDataPoints

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
    header_rows = 7  # = no of rows without empty lines
    for line in lines[0:(header_rows-2)]:
        content = line.split(":")
        content = [i.strip() for i in content]
        if content[1].isdigit():
            header[content[0]] = int(content[1])
        else:
            header[content[0]] = content[1]

    colors = lines[5].split(" ")
    colors = [c.strip(" ") for c in colors]
    colors2 = []
    for c in range(len(colors)):
        if colors[c].isdigit():
            colors2.append(int(colors[c]))
    rgb = np.zeros((header["NrOfPredictors"], 3), dtype=np.int32)
    for c in range(len(colors2)):
        grouping = divmod(c, 3)
        rgb[grouping[0]][grouping[1]] = colors2[c]
    header["Colors"] = rgb

    names = lines[6]
    from_index = 0
    namesarr = []
    for p in range(header["NrOfPredictors"]):
        from_index = names.find('\"', from_index)
        end_index = names.find('\"', from_index+1)
        pname = names[from_index:end_index]
        namesarr.append(pname.replace("\"", ""))
        from_index = (end_index+1)
        p += 1
    header["PredictorNames"] = namesarr

    # SDM data (NrOfDataPoints x NrOfPredictors)
    data = []
    for r, line in enumerate(lines[header_rows:]):
        values = line.split(" ")
        values = [v.strip() for v in values]
        values2 = []
        for v in range(len(values)):
            p = values[v]
            if len(p) > 0:
                # Detect concatenated numbers in *_3DMC.sdm files, such as
                # '0.0310625-0.000387509'
                sign = p.rfind("-", 1)
                if sign > -1:
                    # Detect scientific notation in *_3DMC.sdm files, such as
                    # '5.806e-05'
                    if p.rfind("e") > -1:
                        values2.append(float(p))
                    else:
                        values2.append(float(p[:sign]))
                        values2.append(float(p[sign:]))
                else:
                    values2.append(float(p))
        data.append(values2)

    return header, data
