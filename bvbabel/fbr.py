"""Read, write BrainVoyager FBR file format (binary encoded)"""

import struct

# =============================================================================
def read_fbr(filename):
    """
    Read Brainvoyager FBR file (Binary encoded)

    https://helpdesk.brainvoyager.com/603922-The-Format-of-FBR-Files

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        FBR header data
    groups : list
        Fibers/Streamlines


    Description FBR file format

    Parameter                       Sample value    Description
    -------------                   ---------       -----------
    Magic number (integer 32-bit):  0xa4d3c2b1      Value should be as specified in sample value for binary fiber files

    FileVersion (integer 32-bit):	5               File version of the *.fbr file

    CoordsType (integer 32-bit):    2               BrainVoyager coordinate system: 2 - BVI (default), 1 - SYS, 0 - TAL

    FibersOriginX (float 32-bit):   128             Origin of fibers
    FibersOriginY (float 32-bit):   128
    FibersOriginZ (float 32-bit):   128

    NrOfGroups (int 32-bit):	    1

    [Loop over number of groups:]

        Name (0-terminated 8-bit characters):   "Tracked From VOI: testvoi_ACPC"

        Visible (integer 32-bit):	            1               Boolean value indicating whether the fiber should be shown

        Animate (integer 32-bit):	            -1

        Thickness (float 32-bit):	            0.3             Thickness of the shown fiber in mm

        Color (3 * 8-bit):	                    25 25 127       RGB values for fiber (between 0 and 255)

        NrOfFibers:	                            121

        [Loop over number of fibers/streamlines:]

            NrOfPoints (integer 32-bit):    45

            X positions (float) * number of points

            Y positions (float) * number of points

            Z positions (float) * number of points

            R colour (char) * number of points

            G colour (char) * number of points

            B colour (char) * number of points
    """

    header = dict()
    groups = list()

    with open(filename, 'rb') as f:

        # --- Header fields reading ---
        magic = f.read(4)
        if magic != b'\xa4\xd3\xc2\xb1': # magic number verification
            raise ValueError("FBR file has invalid magic number")

        header['FBRFile'] = filename
        header['MagicNumber'] = magic
        header['FileVersion'] = struct.unpack('<I', f.read(4))[0]
        header['CoordsType'] = struct.unpack('<I', f.read(4))[0]
        fibers_origin = struct.unpack('<3f', f.read(12))
        header['FibersOriginX'] = fibers_origin[0]
        header['FibersOriginY'] = fibers_origin[1]
        header['FibersOriginZ'] = fibers_origin[2]
        header['NrOfGroups'] = struct.unpack('<I', f.read(4))[0]

        # --- Groups reading ---
        for _ in range(header['NrOfGroups']):
            group = dict()
            group_name = bytearray()
            while True:
                char = f.read(1)
                if char == b'\x00': # Group name reading ('0' terminated character)
                    break
                group_name += char
            group['Name'] = group_name.decode('latin-1')
            group['Visible'] = struct.unpack('<I', f.read(4))[0]
            group['Animate'] = struct.unpack('<i', f.read(4))[0]
            group['Thickness'] = struct.unpack('<f', f.read(4))[0]
            group['Color'] = struct.unpack('<3B', f.read(3))
            group['NrOfFibers'] = struct.unpack('<I', f.read(4))[0]

            # Streamlines reading
            fibers = list()
            for _ in range(group['NrOfFibers']):
                fiber = dict()
                nr_of_points = struct.unpack('<I', f.read(4))[0]
                fiber['NrOfPoints'] = nr_of_points

                # Points fiber reading (coordinates)
                points_data = struct.unpack(f'<{3 * nr_of_points}f', f.read(12 * nr_of_points))
                fiber['Xpositions'] = points_data[:nr_of_points]
                fiber['Ypositions'] = points_data[nr_of_points:2 * nr_of_points]
                fiber['Zpositions'] = points_data[2 * nr_of_points:]

                # Colors fiber reading (RGB)
                colors_data = struct.unpack(f'<{3 * nr_of_points}B', f.read(3 * nr_of_points))
                fiber['Rcolour'] = colors_data[:nr_of_points]
                fiber['Gcolour'] = colors_data[nr_of_points:2 * nr_of_points]
                fiber['Bcolour'] = colors_data[2 * nr_of_points:]

                fibers.append(fiber)

            group['Fibers'] = fibers
            groups.append(group)

    return header, groups


def write_fbr(output_filename, header, groups):
    """
    Write BrainVoyager FBR file (Binary encoded)

    Parameters
    ----------
    output_filename : string
        Path to file to be created
    header : dictionary
        Fibers (FBR) header.
    groups : list of dictionaries
        A list of dictionaries. Each dictionary holds a list of fibers/streamlines.

    """

    with open(output_filename, 'wb') as f:

        # --- Header fields writing ---
        f.write(b'\xa4\xd3\xc2\xb1') # magic number writing
        f.write(struct.pack('<I', header['FileVersion']))
        f.write(struct.pack('<I', header['CoordsType']))
        f.write(struct.pack('<3f', header['FibersOriginX'], header['FibersOriginY'], header['FibersOriginZ']))
        f.write(struct.pack('<I', header['NrOfGroups']))

        # --- Groups writing ---
        for group in groups:
            f.write(group['Name'].encode('latin-1') + b'\x00') # group name writing ('0' terminated character)
            f.write(struct.pack('<I', group['Visible']))
            f.write(struct.pack('<i', group['Animate']))
            f.write(struct.pack('<f', group['Thickness']))
            f.write(struct.pack('<3B', *group['Color']))
            f.write(struct.pack('<I', group['NrOfFibers']))

            for fiber in group['Fibers']:
                f.write(struct.pack('<I', fiber['NrOfPoints']))

                # all coordinates X then Y and then Z
                f.write(struct.pack(f'<{fiber["NrOfPoints"]}f', *fiber['Xpositions']))
                f.write(struct.pack(f'<{fiber["NrOfPoints"]}f', *fiber['Ypositions']))
                f.write(struct.pack(f'<{fiber["NrOfPoints"]}f', *fiber['Zpositions']))
                # then all colours R then G and then B
                f.write(struct.pack(f'<{fiber["NrOfPoints"]}B', *fiber['Rcolour']))
                f.write(struct.pack(f'<{fiber["NrOfPoints"]}B', *fiber['Gcolour']))
                f.write(struct.pack(f'<{fiber["NrOfPoints"]}B', *fiber['Bcolour']))