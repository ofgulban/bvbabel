"""Read, write, create BrainVoyager GLM file format."""

import struct
import numpy as np
from bvbabel.utils import read_variable_length_string, read_RGB_bytes
from bvbabel.utils import write_variable_length_string, write_RGB_bytes


# =============================================================================
def read_glm(filename):
    """Read BrainVoyager GLM file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Pre-data headers.
    data : 3D numpy.array
        Image data.

    """
    header = dict()
    with open(filename, 'rb') as f:
        # ---------------------------------------------------------------------
        # GLM Header
        # ---------------------------------------------------------------------
        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2))
        header["File version"] = data

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', f.read(1))
        header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] = int(data)
        data, = struct.unpack('<B', f.read(1))
        header["RFX-GLM (0:std, 1:RFX)"] = int(data)

        # Random effects GLM
        if header["RFX-GLM (0:std, 1:RFX)"] == 1:
            # Expected binary data: int (4 bytes)
            data, = struct.unpack('<i', f.read(4))
            header["Nr subjects"] = int(data)
            data, = struct.unpack('<i', f.read(4))
            header["Nr predictors per subject"] = int(data)

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["Nr time points"] = int(data)
        data, = struct.unpack('<i', f.read(4))
        header["Nr all predictors"] = int(data)
        data, = struct.unpack('<i', f.read(4))
        header["Nr confound predictors"] = int(data)
        data, = struct.unpack('<i', f.read(4))
        header["Nr studies"] = int(data)

        if header["Nr studies"] > 1:
            data, = struct.unpack('<i', f.read(4))
            header["Nr studies with confound info"] = int(data)
            header["Nr confounds per study"] = []
            for i in range(header["Nr studies with confound info"]):
                data, = struct.unpack('<i', f.read(4))
                header["Nr confounds per study"].append(int(data))

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', f.read(1))
        header["Separate predictors (0:no, 1:studies, 2:subjects)"] = int(data)
        data, = struct.unpack('<B', f.read(1))
        header["Time course normalization (1:z transform, 2:baseline z, 3:percent change)"] = int(data)

        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2))
        header["Resolution multiplier (1, 2, 3 times VMR resolution)"] = int(data)

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', f.read(1))
        header["Serial correlation(0:no, 1:AR(1), 2:AR(2))"] = int(data)

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', f.read(4))
        header["Mean serial correlation before correction"] = float(data)
        data, = struct.unpack('<f', f.read(4))
        header["Mean serial correlation after correction"] = float(data)

        # FMR-STC GLM
        if header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] == 0:
            # Expected binary data: short int (2 bytes)
            data, = struct.unpack('<h', f.read(2))
            header["DimX"] = int(data)
            data, = struct.unpack('<h', f.read(2))
            header["DimY"] = int(data)
            data, = struct.unpack('<h', f.read(2))
            header["DimZ"] = int(data)

        # VMR-VTC GLM
        if header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] == 1:
            # Expected binary data: short int (2 bytes)
            data, = struct.unpack('<h', f.read(2))
            header["XStart"] = int(data)
            data, = struct.unpack('<h', f.read(2))
            header["XEnd"] = int(data)
            data, = struct.unpack('<h', f.read(2))
            header["YStart"] = int(data)
            data, = struct.unpack('<h', f.read(2))
            header["YEnd"] = int(data)
            data, = struct.unpack('<h', f.read(2))
            header["ZStart"] = int(data)
            data, = struct.unpack('<h', f.read(2))
            header["ZEnd"] = int(data)

        # SRF-MTC GLM
        if header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] == 2:
            # Expected binary data: int (4 bytes)
            data, = struct.unpack('<i', f.read(4))
            header["Nr vertices"] = int(data)

        # Expected binary data: char (1 byte)
        data, = struct.unpack('<B', f.read(1))
        header["Cortex-based mask (1:(grey matter) mask has been used)"] = data

        # Expected binary data: int (4 bytes)
        data, = struct.unpack('<i', f.read(4))
        header["Nr voxels in mask"] = data

        # Expected binary data: variable-length string
        data = read_variable_length_string(f)
        header["Name of cortex-based mask"] = data

        header["Study info"] = []
        for i in range(header["Nr studies"]):
            header["Study info"].append(dict())
            # Expected binary data: int (4 bytes)
            data, = struct.unpack('<i', f.read(4))
            header["Study info"][i]["Nr time points (volumes) in study"] = data

            # Expected binary data: variable-length string
            data = read_variable_length_string(f)
            header["Study info"][i]["Name of study data"] = data

            if header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] == 2:
                data = read_variable_length_string(f)
                header["Study info"][i]["Name of SSM"] = data

            data = read_variable_length_string(f)
            header["Study info"][i]["Name of SDM"] = data

        data = read_variable_length_string(f)
        header["DEBUG field 00"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 01"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 02"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 03"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 04"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 05"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 06"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 07"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 08"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 09"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 11"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 12"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 13"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 14"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 15"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 16"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 17"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 18"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 19"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 20"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 21"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 22"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 23"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 24"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 25"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 26"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 27"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 28"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 29"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 30"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 31"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 32"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 33"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 34"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 35"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 36"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 37"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 38"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 39"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 40"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 41"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 42"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 43"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 44"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 45"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 46"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 47"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 48"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 49"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 50"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 51"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 52"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 53"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 54"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 55"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 56"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 57"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 58"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 59"] = data
        data = read_variable_length_string(f)
        header["DEBUG field 60"] = data

        if header["RFX-GLM (0:std, 1:RFX)"] == 0:
            # NOTE[Developer Guide - The Format Of GLM Files (v4)]: N x M float,
            # design matrix. Outer loop: N rows (time points); Inner loop: M cols
            # (predictors).
            N = header["Nr time points"]
            M = header["Nr all predictors"]
            temp = np.zeros((N, M), dtype=np.float32)
            for j in range(N):
                for k in range(M):
                    # Expected binary data: float (4 bytes)
                    data, = struct.unpack('<f', f.read(4))
                    temp[j, k] = float(data)
            header["Design matrix"] = np.copy(temp)

            # NOTE[Developer Guide - The Format Of GLM Files (v4)]: M x M float.
            # M rows, cols (predictors): Inverted X'X matrix
            # (inv(transposed DM x DM))
            temp = np.zeros((M, M), dtype=np.float32)
            for j in range(M):
                for k in range(M):
                    # Expected binary data: float (4 bytes)
                    data, = struct.unpack('<f', f.read(4))
                    temp[j, k] = float(data)
            header["Inverted X'X matrix"] = np.copy(temp)

        # ---------------------------------------------------------------------
        # Read GLM data (can represent voxels or vertices)
        # ---------------------------------------------------------------------
        # NOTE[Developer Guide - The Format Of GLM Files (v4)]: The actual data
        # (outer loop: N values (e.g. betas); inner loop: M voxels/vertices).
        if header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] == 0:
            nr_data_points = header["DimX"] * header["DimY"] * header["DimZ"]

        elif header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] == 1:
            range_X = header["XEnd"] - header["XStart"]
            range_Y = header["YEnd"] - header["YStart"]
            range_Z = header["ZEnd"] - header["ZStart"]
            r = header["Resolution multiplier (1, 2, 3 times VMR resolution)"]
            nr_data_points = (range_X // r) * (range_Y // r) * (range_Z // r)

        elif header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] == 2:
            nr_data_points = header["Nr vertices"]

        # NOTE[Developer Guide - The Format Of GLM Files (v4)]: The number of
        # values (and, thus, the number of volume maps) differs with respect to
        # the type of GLM.
        if header["RFX-GLM (0:std, 1:RFX)"] == 1:
            nr_data_point_values = (1 + header["Nr subjects"]
                                    * header["Nr predictors per subject"])

        if header["Serial correlation(0:no, 1:AR(1), 2:AR(2))"] == 0:
            nr_data_point_values = 2 * header["Nr all predictors"] + 2

        # NOTE[Developer Guide - The Format Of GLM Files (v4)]: If AR(1)
        # approach (first-order autoregressive model) has been used to correct
        # serial correlations, one additional volume is stored.
        elif header["Serial correlation(0:no, 1:AR(1), 2:AR(2))"] == 1:
            nr_data_point_values = 2 * header["Nr all predictors"] + 3

        # NOTE[Developer Guide - The Format Of GLM Files (v4)]: If AR(2)
        # approach (second-order autoregressive model) has been used, two
        # additional values are stored.
        elif header["Serial correlation(0:no, 1:AR(1), 2:AR(2))"] == 2:
            nr_data_point_values = 2 * header["Nr all predictors"] + 4

        # NOTE[Faruk]: I am saving this value because it is handy to have. Even
        # though BrainVoyager documentation does not specify it explicitly.
        header["Nr maps"] = nr_data_point_values

        # NOTE[Developer Guide - The Format Of GLM Files (v4)]:
        #     The first value (volume) of the data contains multiple
        # correlation coefficient R indicating the goodness-of-fit for the
        # respective voxel's time course and to allow to calculate the
        # proportion of explained (R^2) and unexplained (1 - R^2) variance.
        #     The second stored value per voxel contains the overall
        # sum-of-squares term (SS_total) that can be used together with the R
        # value to calculate the variance of the residuals.
        #     Following the first two values, the estimated beta values are
        # stored, i.e. one value for each predictor of the design matrix
        # ("Nr all predictors" values).
        #     Following the beta values, another set of "Nr all predictors"
        # values follows containing the sum-of-squares indicating the
        # covariation of each predictor with the time course data (SS_XiY).
        # These values are stored to allow easy calculation of explained
        # variance terms for restricted models (i.e. to allow application of
        # the extra-sum-of-squares principle); these values may be probably
        # ignored (not stored) for custom processing.
        #     The next volume contains the mean value of the (normalized) fMRI
        # time course. Only in case that serial correlation correction has been
        # performed, one or two more values are stored. In case that the AR(1)
        # model has been used the estimated order 1 autocorrelation value
        # (ACF(1) term) is stored for each voxel. In case that the AR(2) model
        # has been used, the two estimated ACF terms are stored, i.e. the data
        # contains one value more than in the case of the AR(1) model.
        data_length = nr_data_point_values * nr_data_points

        data_img = np.zeros(data_length)

        data_img = np.fromfile(f, dtype='<f', count=data_img.size, sep="",
                               offset=0)

        if header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] == 0:
            dims = (nr_data_point_values,
                    header["DimX"], header["DimY"], header["DimZ"])

        elif header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] == 1:
            r = header["Resolution multiplier (1, 2, 3 times VMR resolution)"]
            dim_X = (header["XEnd"] - header["XStart"]) // r
            dim_Y = (header["YEnd"] - header["YStart"]) // r
            dim_Z = (header["ZEnd"] - header["ZStart"]) // r
            dims = (nr_data_point_values, dim_Z, dim_Y, dim_X)

        elif header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] == 2:
            dim = (nr_data_point_values, header["Nr vertices"])

        data_img = np.reshape(data_img, dims)
        data_img = np.transpose(data_img, (1, 2, 3, 0))

        # -------------------------------------------------------------------------
        # NOTE[Faruk]: Developer Guide - The Format Of GLM Files (v4) has further
        # interesting details about calculating standard errors for beta and
        # contrast values. If needed, refer to the PDF in the future.
        # -------------------------------------------------------------------------
    return header, data_img
