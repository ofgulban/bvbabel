'''
BYTES	DATA TYPE	DEFAULT	DESCRIPTION
2	short int	1	NrOfSlices/MapType (t, F, correlation, crosscorrelation etc.) (*1)
2	short int	 	NrOfMaps (equal to NrOfSlices)
2	short int	 	DimY (image dimension in number of pixels)
2	short int	 	DimX (image dimension in number of pixels)
2	short int	 	ClusterSize
4	float	 	Statistical threshold, critical value
4	float	 	Statistical threshold, max value
2	short int	 	NrOfLags (ONLY PRESENT IF MapType = crosscorrelation)
2	short int	9999	Reserved (MUST BE THIS VALUE)
2	short int	3	FileVersion (Current version is 3)
4   int             DF1 (only present if the file version is 3)
4   int             DF2 (only present if the file version is 3)
N	byte	<untitled>	Name of an RTC file (used to compute % signal changes etc.) (*2)
(*2) Variable length, the end of the name is indicated by '0'.
'''

"""Read, write, create BrainVoyager MAP file format."""

import struct
import numpy as np
from bvbabel.utils import read_variable_length_string, read_RGB_bytes
from bvbabel.utils import write_variable_length_string, write_RGB_bytes


# =============================================================================
def read_map(filename):
    """Read BrainVoyager MAP file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Pre-data and post-data headers.
    data : 3D numpy.array
        Image data.

    """
    header = dict()
    with open(filename, 'rb') as f:
        # ---------------------------------------------------------------------
        # NR-MAP Header (Version 2)
        # ---------------------------------------------------------------------

        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2))
        header["MapType"] = 't-values'
        header["NrOfSlices"] = int(data)
        data, = struct.unpack('<h', f.read(2))
        header["NrOfMaps"] = int(data)
        data, = struct.unpack('<h', f.read(2))
        header["DimX"] = int(data)
        data, = struct.unpack('<h', f.read(2))
        header["DimY"] = int(data)
        data, = struct.unpack('<h', f.read(2))
        header["ClusterSize"] = int(data)

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', f.read(4))
        header["Min"] = data  # 	Statistical threshold, critical value
        data, = struct.unpack('<f', f.read(4))
        header["Max"] = data # 	Statistical threshold, max value

        # Expected binary data: short int (2 bytes)
        if header["MapType"] == 'crosscorrelation':
	        data, = struct.unpack('<h', f.read(2))
	        header["NrOfLags"] = int(data)

        # Expected binary data: short int (2 bytes) 
        data, = struct.unpack('<h', f.read(2)) # Reserved field 9999
        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2)) # Version 3

        data, = struct.unpack('<i', f.read(4)) # DF1
        header["df1"] = int(data)

        data, = struct.unpack('<i', f.read(4)) # DF2
        header["df2"] = int(data)

        # Expected binary data: variable-length string
        data = read_variable_length_string(f)  # Reserved field
        header["RTCName"] = data

        # ---------------------------------------------------------------------
        # Read MAP image data
        # ---------------------------------------------------------------------
        # A map file contains NrOfMaps (= NrOfSlices) 2D statistical images. Each image contains DimY*DimX data points.
        # Each data point (statistical value) is represented in 4 bytes (float). 
        # Each slice is preceded by a 2 byte (short int) value representing the slice index (i.e. '0' for slice 1 and 'NrOfMaps-1' for the last slice). 
        # There are some additional informations about MAP files which are specific to correlation and cross-correlation maps.
        #
        
        data_img = []#np.zeros( header['NrOfSlices'] * header['DimY'] * header['DimX'])

        for s in range(header['NrOfSlices']):

            # Expected binary data: short int (2 bytes)
            data, = struct.unpack('<h', f.read(2)) #Slice number
            data_img.append(np.reshape(np.fromfile(f, dtype='<f', count=header['DimY'] * header['DimX'], sep="", offset=0), (header['DimX'],header['DimY']))[:,:,None]) # slice data

            #print('Slice: ', data)

            temp_img = []
            #for y in range(header['DimY']):
            #    for x in range(header['DimX']):
            #        data, = struct.unpack('<f', f.read(4))
            #       temp_img.append(data)
            #data_img.append(np.reshape(temp_img,(header['DimY'],header['DimX']))[:,:,None])

        # -----------------------------------------------------------------

    data_img = np.concatenate(data_img, axis=2) # stuck the slices
    data_img = np.transpose(data_img, (1, 0, 2))
    data_img = data_img[::-1, ::-1,:]  # Flip BV axes

    return header, data_img
