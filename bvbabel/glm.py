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
    data_R2 : 3D (if volume) OR 1D (if vertices) numpy.array
        Multiple correlation coefficient R indicating the goodness-of-fit for
        the respective voxel's time course and to allow to calculate the
        proportion of explained (R^2) and unexplained (1 - R^2) variance.
    data_SS : 3D (if volume) OR 1D (if vertices) numpy.array
        Sum-of-squares term (SS_total) that can be used together with the R
        value to calculate the variance of the residuals.
    data_beta : 4D (if volume) OR 2D (if vertices) numpy.array
        Estimated beta values. One value for each predictor of the design
        matrix ("Nr all predictors" values).
    data_XY = 4D (if volume) OR 2D (if vertices) numpy.array
        Sum-of-squares indicating the covariation of each predictor with the
        time course data (SS_XiY). These values are stored to allow easy
        calculation of explained variance terms for restricted models (i.e. to
        allow application of the extra-sum-of-squares principle); these values
        may be ignored (not stored) for custom processing.
    data_ARlag : 3D or 4D (if volume) OR 1D or 2D (if vertices) numpy.array
        Auto-regression lag value. If "serial correlation" is 1, this will be a
        3D numpy.array (if volume) or 1D numpy.array (if vertices). If "serial
        correlation" is 2, this will be a 4D numpy.array (if volume) or 2D
        numpy.array (if vertices). If "serial correlation" is zero, this will
        be a 3D numpy.array (if volume) or 1D numpy.array (if vertices)
        containing all zeros (can be ignored)

    Notes
    -----
        - NOTE[Faruk]: "Developer Guide - The Format Of GLM Files (v4)" has
    interesting details about calculating standard errors for beta and contrast
    values. In order to retain this extra information, I am including these
    notes below.
        - The (non-RFX) GLM file stores enough values to allow calculation of
    standard errors for beta and contrast values for each voxel. The stored
    multiple correlation coefficient R (data_R2) together with the overall
    sum-of-squares term (data_SS) can be used to calculate the variance of
    the residuals as follows:
        `VAR_residuals = data_SS * (1 - data_R2) / (header["Nr time points"]  - header["Nr all predictors"])`
    Together with the stored inverted X'X matrix, this allows calculating the
    standard error for any beta or contrast t value using the usual equation
    (c is the contrast vector and b is the voxel's vector of stored beta
    values):
        `t = c'b / sqrt(VAR_residuals * c' * header["Inverted X'X matrix"] * c)`
    However, note that in case of performed serial correlation correction, the
    inverted X'X matrix needs to be recalculated for each voxel from the stored
    design matrix X using the voxel-specific autocorrelation function term(s);
    furthermore the number of time points (NTimePoints) needs to be corrected
    [subtraction of 1 for AR(1) model, subtraction of 2 for AR(2) model].

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

            # NOTE[Faruk]: Conflicting information in the documents. This might
            # be called RTC filename
            data = read_variable_length_string(f)
            header["Study info"][i]["Name of SDM"] = data

        # ---------------------------------------------------------------------
        header["Predictor info"] = list()
        for i in range(header["Nr all predictors"]):
                header["Predictor info"].append(dict())

                # Expected binary data: variable-length string
                data = read_variable_length_string(f)
                header["Predictor info"][i]["Name (internal)"] = data
                data = read_variable_length_string(f)
                header["Predictor info"][i]["Name (custom)"] = data

                # Expected binary data: char (1 byte) x 3
                data = read_RGB_bytes(f)
                header["Predictor info"][i]["Color"] = data

                # TODO: Unknown bytes, ask to senior dev. for documentation
                f.read(9)

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
        data_all = np.zeros(data_length, dtype=np.float32)
        data_all = np.fromfile(f, dtype='<f', count=data_all.size, sep="",
                               offset=0)

        if header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] == 0:
            dims = (nr_data_point_values,
                    header["DimZ"], header["DimY"], header["DimX"])

        elif header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] == 1:
            r = header["Resolution multiplier (1, 2, 3 times VMR resolution)"]
            dim_X = (header["XEnd"] - header["XStart"]) // r
            dim_Y = (header["YEnd"] - header["YStart"]) // r
            dim_Z = (header["ZEnd"] - header["ZStart"]) // r
            dims = (nr_data_point_values, dim_Z, dim_Y, dim_X)

        elif header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC"] == 2:
            dim = (nr_data_point_values, header["Nr vertices"])

        data_all = np.reshape(data_all, dims)
        data_all = np.transpose(data_all, (1, 3, 2, 0))
        data_all = data_all[::-1, ::-1, ::-1, :]

        # ---------------------------------------------------------------------
        # Parse into separate maps.
        # ---------------------------------------------------------------------
        # Multiple regression R values (multipleRegrR)
        data_R2 = data_all[..., 0]

        # Sum of squares values (mCorrSS)
        data_SS = data_all[..., 1]

        # Beta values (BetaMaps)
        p = header["Nr all predictors"]
        data_beta = data_all[..., 2:2+p]

        # XY (Fitted data after regression, only present in File versions > 1)
        data_XY = data_all[..., 2+p:2+p+p]

        # arLag1 (Auto-regression lag value)
        if header["Serial correlation(0:no, 1:AR(1), 2:AR(2))"] == 1:
            data_ARlag = data_all[..., 2+p+p:2+p+p+1]
        elif header["Serial correlation(0:no, 1:AR(1), 2:AR(2))"] == 2:
            data_ARlag = data_all[..., 2+p+p:2+p+p+2]
        else:
            data_ARlag = np.zeros(data_R2.shape)  # placeholder array

    return (header, data_R2, data_SS, data_beta, data_XY, data_ARlag)
