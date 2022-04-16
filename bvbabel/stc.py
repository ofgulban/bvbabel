"""Read, write, create Brainvoyager STC file format."""

import numpy as np


# =============================================================================
def read_stc(filename, nr_slices, nr_volumes, res_x, res_y, data_format=2):
    """Read Brainvoyager STC file.

    Parameters
    ----------
    filename : string
        Path to file.
    nr_slices: integer
        Number of slices in each measurement. Referred to as "NrOfSlices"
        within the FMR text file.
    nr_volumes: integer
        Number of measurements (also called volumes or TRs). Referred to as
        "NrOfVolumes" within the FMR text file.
    res_x: integer
        Number of voxels along each row in each slice. Referred to as
        "ResolutionX" within the FMR text file.
    res_y: integer
        Number of voxels along each column in each slice. Referred to as
        "ResolutionY" within the FMR text file.
    data_format: integer, 1 or 2
        Each data element (intensity value) is represented either in 2 bytes
        (unsigned short) or in 4 bytes (float, default) as determined by the
        "DataStorageFormat" entry in the FMR file.

    Returns
    -------
    data : 4D numpy.array, (x, y, slices, time)
        Image data.

    """
    if data_format == 1:
        data_img = np.fromfile(filename, dtype="<H", count=-1, sep="",
                               offset=0)
    elif data_format == 2:
        data_img = np.fromfile(filename, dtype="<f", count=-1, sep="",
                               offset=0)

    data_img = np.reshape(data_img, (nr_slices, nr_volumes, res_x, res_y))
    data_img = np.transpose(data_img, (3, 2, 0, 1))
    data_img = data_img[:, ::-1, ::, :]  # Flip BV axes

    return data_img
