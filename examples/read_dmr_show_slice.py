"""Read BrainVoyager dmr, show difference image and save figure to disk."""

import os
import numpy as np
import matplotlib.pyplot as plt
import bvbabel

FILE = '/Users/hester/Data/Testdata_PluginsScripts/DTI/bv224/human31dir_bv224.dmr'
save_figure = True

# =============================================================================

# Load dmr    
header, data = bvbabel.dmr.read_dmr(FILE)

# Make slices
selected_slice = round(header["NrOfSlices"]/2)
slice_dmr = data[:,:,selected_slice,1]
slice_dmr2 = data[:,:,selected_slice,header["NrOfVolumes"]-1]
slice_dmr3 = np.subtract(slice_dmr, slice_dmr2)

# Display and save to disk
plt.figure()
ax1 = plt.subplot(1, 3, 1)
plt.imshow(slice_dmr, cmap='bone')
ax2 = plt.subplot(1, 3, 2)
plt.imshow(slice_dmr2, cmap='bone')
ax3 = plt.subplot(1, 3, 3)
plt.imshow(slice_dmr3, cmap='bone')
plt.tight_layout()
if save_figure:
    plt.savefig(os.path.splitext(FILE)[0], dpi=200)
plt.show()
