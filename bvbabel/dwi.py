"""Read BrainVoyager DWI file format."""

import struct
import numpy as np


# =============================================================================
def read_dwi(filename, nr_slices, nr_directions, res_x, res_y, data_type=2, rearrange_data_axes=True):
    """Read BrainVoyager diffusion weighted imaging (DWI) file.

    Parameters
    ----------
    filename : string
        Path to file.
    nr_slices: integer
        Number of slices in each measurement. Referred to as "NrOfSlices"
        within the FMR text file.
    nr_directions: integer
        Number of measurements (also called volumes or TRs). Referred to as
        "NrOfVolumes" within the DMR text file.
    res_x: integer
        Number of voxels along each row in each slice. Referred to as
        "ResolutionX" within the FMR text file.
    res_y: integer
        Number of voxels along each column in each slice. Referred to as
        "ResolutionY" within the FMR text file.
    data_type: integer, 1 or 2
        Each data element (intensity value) is represented either in 2 bytes
        (unsigned short) or in 4 bytes (float, default) as determined by the
        "DataType" entry in the DMR file.
    rearrange_data_axes : bool
        When 'False', axes are intended to follow LIP+ terminology used
        internally in BrainVoyager (however see the notes below):
            - 1st axis is Right to "L"eft.
            - 2nd axis is Superior to "I"nferior.
            - 3rd axis is Anterior to "P"osterior.
        When 'True' axes are intended to follow nibabel RAS+ terminology:
            - 1st axis is Left to "R"ight.
            - 2nd axis is Posterior to "A"nterior.
            - 3rd axis is Inferior to "S"uperior.

    Returns
    -------
    data : 4D numpy.array, (x, y, slices, directions)
        Image data.

    """
    if data_type == 1:
        data_img = np.fromfile(filename, dtype="<H", count=-1, sep="",
                               offset=0)
    elif data_type == 2:
        data_img = np.fromfile(filename, dtype="<f", count=-1, sep="",
                               offset=0)

    data_img = np.reshape(data_img, (nr_slices, nr_directions, res_x, res_y))

    # TODO[Faruk]: I need to double check this part with various data
    if rearrange_data_axes is True:
        data_img = np.transpose(data_img, (3, 2, 0, 1))
        data_img = data_img[:, ::-1, :, :]  # Flip BV axes

    return data_img
