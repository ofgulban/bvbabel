"""Read Brainvoyager sdm (single subject design matrix / motion estimates)."""

import bvbabel
import numpy
import sys


#FILE = '/Volumes/ELEMENTS/Data/Data_PluginsTesting_New/Data_Python_bvbabel/SDM/FacesHousesDesignMatrix.sdm'
FILE = '/Volumes/ELEMENTS/Data/Data_PluginsTesting_New/Data_Python_bvbabel/SDM/sub-01_ses-04_task-blocked_run-1_bold_3DMC.sdm'

# =============================================================================

# Load design matrix
header, data = bvbabel.sdm.read_sdm(FILE)

# Print header information
print("\nSDM header")
for key, value in header.items():
    print("  ", key, ":", value)

print("\nSDM data")
txt = ''     
for datapoint in range(header["NrOfDataPoints"]):
    for predno in range(header["NrOfPredictors"]):
        txt += ' ' + "{:>10.6f}".format(data[datapoint][predno])
    txt += '\n'
print(txt)        
    
print("Finished.")
