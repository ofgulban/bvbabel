"""Read BrainVoyager MDM file format."""

# =============================================================================
def read_mdm(filename):
    """Read BrainVoyager MDM file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Multi subjects design matrix (MDM) header. 
    data : list
        Each element contains a dictionary that contains the information of
        a single study.

    """
    # Read non-empty lines of the input text file
    with open(filename, 'r') as f:
        lines = [r for r in (line.strip() for line in f) if r]

    # MDM header
    header = dict()
    header_rows = 7  # Nr of rows without empty lines
    for line in lines[0:header_rows]:
        content = line.split(":")
        content = [i.strip() for i in content]
        if content[1].isdigit():
            header[content[0]] = int(content[1])
        else:
            header[content[0]] = content[1]

    # -----------------------------------------------------------------------------
    # MDM data
    data = list()
    studies_row = 7
    for line in lines[studies_row:]:
        temp = dict()
        content = line.split('" "')
        content = [i.strip('"') for i in content]
        temp["PathNameData"] = content[-2]
        temp["PathNameSDM"] = content[-1]
        if header["TypeOfFunctionalData"] == 'MTC':
            temp["PathNameSSM"] = content[-3]
        data.append(temp)

    return header, data


def write_mdm(filename, header, data_mdm):
    """Protocol to write BrainVoyager MDM file.

    Parameters
    ----------
    filename : string
        Path to file.
    header : dictionary
        Multi subjects design matrix (MDM) header. 
    data_mdm : list
        Each element contains a dictionary that contains the information of
        a single study.

    """
    with open(filename, 'w') as f:
        f.write("\n")
        data = header["FileVersion"]
        f.write("FileVersion:          {}\n".format(data))
        data = header["TypeOfFunctionalData"]
        f.write("TypeOfFunctionalData: {}\n".format(data))
        f.write("\n")
        
        data = header["RFX-GLM"]
        f.write("RFX-GLM:              {}\n".format(data))
        f.write("\n")
        
        data = header["PSCTransformation"]
        f.write("PSCTransformation:    {}\n".format(data))
        data = header["zTransformation"]
        f.write("zTransformation:      {}\n".format(data))
        data = header["SeparatePredictors"]
        f.write("SeparatePredictors:   {}\n".format(data))
        f.write("\n")

        data = header["NrOfStudies"]
        f.write("NrOfStudies:          {}\n".format(data))

        # ---------------------------------------------------------------------
        # Write data
        nr_rows = header["NrOfStudies"]
        for i in range(nr_rows):
            if header["TypeOfFunctionalData"] == 'MTC': 
                f.write('\"{}\" \"{}\" \"{}\"'.format(data_mdm[i]["PathNameSSM"], data_mdm[i]["PathNameData"], data_mdm[i]["PathNameSDM"]))
            else:
                f.write('\"{}\" \"{}\"'.format(data_mdm[i]["PathNameData"], data_mdm[i]["PathNameSDM"]))
            f.write("\n")


            
def create_mdm(surface_data=False):
    """Create BrainVoyager MDM file with default values.

    Parameters
    ----------
    surface_data : bool
        'False': an MDM file for VTC data is created
        'True': an MDM file for MTC data is created
        
    Returns
    -------
    header : dictionary
        Multi subjects design matrix (MDM) header.
    data : list
        Each element contains a dictionary that contains the information of
        a single study.
        
    Notes on header values
    --------
    FFX (fixed effects) : RFX-GLM = 0, SeparatePredictors = 0
    SPST (separate studies) : RFX-GLM = 0, SeparatePredictors = 1
    SPSB (separate subjects): RFX-GLM = 0, SeparatePredictors = 2
    RFX (random effects): RFX-GLM = 1, SeparatePredictors = 2
    
    PT (percent signal change transformation of voxel time courses): PSCTransformation = 1, zTransformation = 0
    ZT (z-transformation of voxel time courses): 
    ZTB (z-transformation using only baseline segments): PSCTransformation = 0, zTransformation = 1

    """
    header = dict()
    header["FileVersion"] =  3
    if surface_data:
        header["TypeOfFunctionalData"] = 'MTC'
    else:
        header["TypeOfFunctionalData"] = 'VTC'
    header["RFX-GLM"] = 1
    header["PSCTransformation"] = 1
    header["zTransformation"] = 0
    header["SeparatePredictors"] = 2
    header["NrOfStudies"] = 1

    # -------------------------------------------------------------------------
    # Create random predictors as data
    data = list()
    temp = dict()
    temp["PathNameSDM"] = "/Path/To/SDMfile"
    if header["TypeOfFunctionalData"] == 'MTC':
        temp["PathNameSSM"] = "/Path/To/SSMfile"
        temp["PathNameData"] = "/Path/To/MTCfile"
    else:
        temp["PathNameData"] = "/Path/To/VTCfile"
    data.append(temp)
        
    return header, data
