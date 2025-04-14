""" Read BrainVoyager FBR file format."""

import numpy as np
import re

# =============================================================================
def read_fbr(filename):    
    """Read Brainvoyager FBR file

    https://helpdesk.brainvoyager.com/603922-The-Format-of-FBR-Files

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Fiber (FBR) header. 
    data : 
        Fiber points


    Description FBR file format
 	
    Parameter       Sample value     Description 	
    -------------   ---------        -----------
	 
    FileVersion:	4               File version of the *.fbr file

    CoordsType:     BV I            BrainVoyager coordinate system

    FibersOriginX:  128             Origin of fibers (FileVersion 4)
    FibersOriginY:  128
    FibersOriginZ:  128

    NrOfGroups:	    1
	 
    Name:	        "Tracked From VOI: testvoi_ACPC"
	 
    Visible:	    1               Boolean value indicating whether the fiber should be shown
    Animate:	    -1
	 
    Thickness:	    0.3             Thickness of the shown fiber in mm (?)
    Color:	        25 25 127       RGB values for fiber (between 0 and 255)
    NrOfFibers:	    121
	 
    [Loop over number of fibers:]	

        NrOfPoints:	    <int>
        (3x float 3x int)	101.209 128.266 120.192     156 148 135

        For example: 

        NrOfPoints:    2
        101.209 128.266 120.192    156 148 135
        101.5 128 120.5    156 148 135
	 

    Newer information (see DTI Getting Started Guide 1.1):

        This is the coordinate system in the OpenGL/3D Viewer window.
        Origin: [x, y, z] = 0.5*VMR slice X-resolution, 0.5*VMR slice Y-resolution, 0.5*number of slices 
        x-axis: anterior to posterior 0 to X-resolution 
        y-axis: superior to inferior 0 to Y-resolution 
        z-axis: right to left 0 to Z-resolution

    """

    # Read non-empty lines of the input text file
    with open(filename, 'r') as f:
        lines = [r for r in (line.strip() for line in f) if r]

    # FBR header
    header = dict()
    n_header_rows = 12 # = no of rows without empty lines
    for line in lines[0:(n_header_rows)]:#-2)]:
        content = line.split(":")
        content = [i.strip() for i in content]
        if content[1].isdigit():
            header[content[0]] = int(content[1])
        else:
            header[content[0]] = content[1]

    colors = lines[10].split(" ")
    colors = [c.strip(" ") for c in colors]
    colors2 = []
    for c in range(len(colors)):
        if colors[c].isdigit():
            colors2.append(int(colors[c]))               
    header["Color"] = colors2

    count_fbr = -1
    data_fbr = list()
    p = re.compile(r'\d+(\.\d+)?$') # regular expression for detecting floats, isdigits() does not work
    for line in lines[n_header_rows:]: # loop from end of header to end of file

        if "NrOfPoints" in line:   
            content = line.split(":")
            content = [i.strip() for i in content]
            count_fbr += 1
            data_fbr.append(dict())
            data_fbr[count_fbr]["NrOfPoints"] = int(content[1])
            data_fbr[count_fbr]["Points"] = []  # prepare for coordinates
        else: # points content
            values = line.split(" ")
            points = []
            for v in values:
                if v.isdigit():
                    points.append(int(v.strip()) ) 
                elif p.match(v):    
                    points.append(float(v.strip()) ) 
            data_fbr[count_fbr]["Points"].append(points)

    return header, data_fbr            



def write_fbr(filename, header, data_fbr):
    """Function to write BrainVoyager FBR file.

    Parameters
    ----------
    filename : string
        Path to file.
    header : dictionary
        Fibers (FBR) header.
    data_fbr : list of dictionaries
        A list of dictionaries. Each dictionary holds coordinates of a fiber.

    """

    with open(filename, 'w') as f:

        data = header["FileVersion"]
        f.write("FileVersion:\t{}\n".format(data))
        data = header["CoordsType"]
        f.write("CoordsType:\t{}\n".format(data))
        data = header["FibersOriginX"]
        f.write("FibersOriginX:\t{}\n".format(data))
        data = header["FibersOriginY"]
        f.write("FibersOriginY:\t{}\n".format(data))
        data = header["FibersOriginZ"]
        f.write("FibersOriginZ:\t{}\n".format(data))      
        f.write("\n")
        data = header["NrOfGroups"]
        f.write("NrOfGroups:\t{}\n".format(data))        
        f.write("\n")
        data = header["Name"]
        f.write("Name:\t\t{}\n".format(data))   
        data = header["Visible"]
        f.write("Visible:\t{}\n".format(data))           
        data = header["Animate"]
        f.write("Animate:\t{}\n".format(data))   
        data = header["Thickness"]
        f.write("Thickness:\t{}\n".format(data))   
        data = header["Color"]
        f.write("Color:\t\t{} {} {}\n".format(data[0], data[1], data[2]))
        f.write("\n")
        data = header["NrOfFibers"]
        f.write("NrOfFibers:\t{}\n".format(data))     
        f.write("\n")

        # ---------------------------------------------------------------------
        # FBR data

        for p in data_fbr:
            data = p["NrOfPoints"]
            f.write("NrOfPoints:\t{}\n".format(data))
            data = p["Points"]
            for d in data:
                f.write("{:.3f} {:.3f} {:.3f}    {:n} {:n} {:n}\n".format(d[0], d[1], d[2], d[3], d[4], d[5]))
            f.write("\n")

