"""Read, write, create BrainVoyager GLM file format (v4)."""

import struct
import numpy as np
from bvbabel.utils import read_variable_length_string, read_RGB_bytes
from bvbabel.utils import write_variable_length_string, write_RGB_bytes


# =============================================================================
def read_glm(filename):
    """Read BrainVoyager GLM file v4.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Pre-data headers.
    data_R2 : 3D (if volume) OR 1D (if vertices) numpy.array
        For a standard (non-RFX) GLM, multiple correlation coefficient R,
        indicating the goodness-of-fit for the respective voxel's time course. 
        For an RFX GLM, this contains the 'rfxGlobalMap' currently unused by 
        BrainVoyager. The interpretation of its values is not specified in the 
        'Developer Guide - The Format Of GLM Files (v4)' documentation.
    data_SS : 3D (if volume) OR 1D (if vertices) numpy.array or None
        Sum-of-squares term (SS_total) for a standard GLM. 'None' for a RFX
        GLM because this map is not stored in RFX data.
    data_beta : 4D (if volume) OR 2D (if vertices) numpy.array
        Estimated beta values. For a standard GLM, one value is returned for
        each predictor of the design matrix. For a RFX GLM, the final dimension
        contains the subject/predictor beta maps in file order.
    data_SS_XiY : 4D (if volume) OR 2D (if vertices) numpy.array or None
        Sum-of-squares indicating the covariation of each predictor with the
        time course data (SS_XiY). These values are stored to allow easy
        calculation of explained variance terms for restricted models (i.e. to
        allow application of the extra-sum-of-squares principle); these values
        may be ignored (not stored) for custom processing. 'None' for a RFX GLM.
    data_meantc : 3D (if volume) OR 1D (if vertices) numpy.array or None
        Mean value of the (normalized) fMRI time course. 'None' for a RFX GLM.
    data_ARlag : 3D or 4D (if volume) OR 1D or 2D (if vertices) numpy.array or None
        Auto-regression lag value. If "serial correlation" is 1, this will be a
        3D numpy.array (if volume) or 1D numpy.array (if vertices). If "serial
        correlation" is 2, this will be a 4D numpy.array (if volume) or 2D
        numpy.array (if vertices). If "serial correlation" is zero, this will
        be a 3D numpy.array (if volume) or 1D numpy.array (if vertices)
        containing all zeros (can be ignored). 'None' for a RFX GLM.

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
        header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC)"] = int(data)
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
        if header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC)"] == 0:
            # Expected binary data: short int (2 bytes)
            data, = struct.unpack('<h', f.read(2))
            header["DimX"] = int(data)
            data, = struct.unpack('<h', f.read(2))
            header["DimY"] = int(data)
            data, = struct.unpack('<h', f.read(2))
            header["DimZ"] = int(data)

        # VMR-VTC GLM
        if header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC)"] == 1:
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
        if header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC)"] == 2:
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

            if header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC)"] == 2:
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

                # NOTE[Judith]: Each predictor stores 12 color bytes as four RGB
                # triplets. These triplets seem to encode [R, 0, 0], [0, G, 0],
                # [0, 0, B], [0, 0, 0]. Preserve all 12 bytes exactly as 
                # stored in the GLM file. The exact meaning is not specified 
                # in the v4 format description. 
                # Color is the (4, 3) uint8 header entry.
                color = np.zeros((4, 3), dtype=np.ubyte)
                for j in range(4):
                    color[j, :] = read_RGB_bytes(f)
                header["Predictor info"][i]["Color"] = color

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
        # NOTE[Judith]: Validate the GLM type and calculate the number of spatial
        # data points in one place, to detect inconsistent bounding-box values.
        # The VTC dimensions must be divisible by the resolution multiplier.
        # Avoids silent flooring since this can misalign the file.
        glm_type = header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC)"]
        if glm_type == 0:
            nr_data_points = header["DimX"] * header["DimY"] * header["DimZ"]

        elif glm_type == 1:
            range_X = header["XEnd"] - header["XStart"]
            range_Y = header["YEnd"] - header["YStart"]
            range_Z = header["ZEnd"] - header["ZStart"]
            r = header["Resolution multiplier (1, 2, 3 times VMR resolution)"]
            if r <= 0:
                raise ValueError("GLM resolution multiplier must be positive.")
            if (range_X % r) or (range_Y % r) or (range_Z % r):
                raise ValueError(
                    "GLM VTC bounding-box ranges are not divisible by the "
                    "resolution multiplier."
                )
            dim_X = range_X // r
            dim_Y = range_Y // r
            dim_Z = range_Z // r
            nr_data_points = dim_X * dim_Y * dim_Z

        elif glm_type == 2:
            nr_data_points = header["Nr vertices"]

        else:
            raise ValueError("Unsupported GLM type: {}".format(glm_type))

        # NOTE[Judith]: Keep RFX and standard map-count separate.
        # RFX files contain one global map plus
        # one beta map for each subject/predictor combination. 
        rfx_glm = header["RFX-GLM (0:std, 1:RFX)"] == 1
        serial_correlation = header[
            "Serial correlation(0:no, 1:AR(1), 2:AR(2))"
        ]

        if rfx_glm:
            nr_data_point_values = (
                1
                + header["Nr subjects"]
                * header["Nr predictors per subject"]
            )
        else:
            if serial_correlation not in (0, 1, 2):
                raise ValueError(
                    "Unsupported serial-correlation flag: {}".format(
                        serial_correlation
                    )
                )

            # The v4 table gives 2*NAllPredictors+2 as the base count, but its
            # detailed layout also stores one mean-time-course map. Hence: 
            # R + SS + beta + SS_XiY + mean, plus one/two AR maps when applicable.
            nr_data_point_values = (
                2 + 2 * header["Nr all predictors"] + 1 + serial_correlation
            )

        # NOTE[Faruk]: I am saving this value because it is handy to have. Even
        # though BrainVoyager documentation does not specify it explicitly.
        header["Nr maps"] = nr_data_point_values


        # NOTE[Judith]: Read the expected number of float32 values.
        # Check that the GLM data section contains the expected number of values.
        expected_values = nr_data_point_values * nr_data_points
        
        data_all = np.fromfile(
            f, dtype='<f4', count=expected_values
        )
        
        if data_all.size != expected_values:
            raise ValueError(
                "Incomplete GLM data section: expected {} float32 values, "
                "but read {}.".format(expected_values, data_all.size)
            )
        # Check that no unexpected bytes remain after the GLM data.
        if f.read(1):
            raise ValueError(
                "Unexpected additional bytes at the end of the GLM file."
            )
            
        # NOTE[Judith]: The surface data is a 2-D (maps, vertices) array on disk. 
        # The previous 'dim'/'dims' typo prevented reading any SRF file.
        if glm_type == 0:
            dims = (nr_data_point_values,
                    header["DimZ"], header["DimY"], header["DimX"])

        elif glm_type == 1:
            dims = (nr_data_point_values, dim_Z, dim_Y, dim_X)

        elif glm_type == 2:
            dims = (nr_data_point_values, header["Nr vertices"])

        data_all = np.reshape(data_all, dims)
        if glm_type == 2:
            # SRF-MTC: (maps, vertices) -> (vertices, maps).
            data_all = np.transpose(data_all, (1, 0))
        else:
            # FMR-STC / VMR-VTC: retain original orientation.
            data_all = np.transpose(data_all, (1, 3, 2, 0))
            data_all = data_all[::-1, ::-1, ::-1, :]

        # ---------------------------------------------------------------------
        # Parse into separate maps.
        # ---------------------------------------------------------------------
        # NOTE[Judith]: RFX data has a different layout from the standard GLM
        # data. 
        if rfx_glm:
            # The first RFX map is called "rfxGlobalMap" in BrainVoyager's
            # GLM v1-3 documentation (2018), where it is described as unused.
            # Its meaning in newer GLM versions is not established here.
            #
            # Return this map in data_R2 to preserve the existing bvbabel
            # return structure. For RFX GLMs, data_R2 does not represent R².
            data_R2 = data_all[..., 0]
            nr_rfx_betas = (
                header["Nr subjects"] * header["Nr predictors per subject"]
            )
            data_beta = data_all[..., 1:1+nr_rfx_betas]
            data_SS = None
            data_SS_XiY = None
            data_meantc = None
            data_ARlag = None

        else:
            # NOTE[Developer Guide - The Format Of GLM Files (v4)]:
            # The following map layout applies to standard (non-RFX) GLMs.
            #
            # The first value (volume) of the data contains the multiple
            # correlation coefficient R indicating the goodness-of-fit for the
            # respective voxel's time course and allowing calculation of the
            # proportion of explained (R^2) and unexplained (1 - R^2) variance.
            #
            # The second stored value contains the overall sum-of-squares
            # term (SS_total).
            #
            # Following the first two values, the estimated beta values are
            # stored, followed by the SS_XiY values for all predictors.
            #
            # The next volume contains the mean time-course value.
            # If serial correlation correction was performed, one additional
            # map is stored for AR(1), or two additional maps for AR(2).
            
            
            # Multiple regression R values (multipleRegrR)
            data_R2 = data_all[..., 0]

            # Sum of squares values (mCorrSS)
            data_SS = data_all[..., 1]

            # Beta values (BetaMaps)
            p = header["Nr all predictors"]
            data_beta = data_all[..., 2:2+p]

            # Sum-of-squares indicating the covariation of each predictor with
            # the time course (SS_XiY).
            data_SS_XiY = data_all[..., 2+p:2+p+p]

            # NOTE[Judith]: Index the mean map directly so that only the map axis is
            # removed. 
            mean_index = 2 + p + p
            data_meantc = data_all[..., mean_index]

            # Auto-regression lag value(s). Direct indexing for AR(1) returns the
            # documented 3-D volume / 1-D surface shape; AR(2) keeps a lag axis.
            ar_start = mean_index + 1
            if serial_correlation == 1:
                data_ARlag = data_all[..., ar_start]
            elif serial_correlation == 2:
                data_ARlag = data_all[..., ar_start:ar_start+2]
            else:
                data_ARlag = np.zeros(data_R2.shape, dtype=np.float32)

    return (header, data_R2, data_SS, data_beta, data_SS_XiY, data_meantc, data_ARlag)


# =============================================================================
# NOTE[Judith]: Writing GLMs.
# Map data is written one map at a time to avoid constructing another 
# full 4-D array.
def write_glm(filename, header, data_R2, data_SS, data_beta, data_SS_XiY,
              data_meantc, data_ARlag=None):
    """Write a BrainVoyager GLM using the seven values returned by read_glm.

    Parameters
    ----------
    filename : str or path-like
        Output file path (existing files are overwritten).
    header : dict
        Header returned by 'read_glm' or an equivalent complete GLM header.
    data_R2, data_SS, data_beta, data_SS_XiY, data_meantc, data_ARlag : arrays
        in the same order as returned by 'read_glm'.
        For RFX, 'data_R2' is the first (global) RFX map, 'data_beta' 
        holds the subject/predictor beta maps, and all other map arguments 
        should be 'None'. 
        For standard (non-RFX) GLMs, 'data_ARlag' is optional only when 
        serial correlation is zero.

    Notes
    -----
    FMR-STC and VMR-VTC arrays use (Z, X, Y[, maps]) orientation;
    SRF-MTC arrays use (vertices[, maps]). Float maps and design matrices are
    written as little-endian float32, with maps stored first on disk.
    """
    glm_type = header["Type (0: FMR-STC, 1:VMR-VTC, 2:SRF-MTC)"]
    rfx_flag = header["RFX-GLM (0:std, 1:RFX)"]
    serial_correlation = header[
        "Serial correlation(0:no, 1:AR(1), 2:AR(2))"
    ]
    nr_predictors = header["Nr all predictors"]
    nr_studies = header["Nr studies"]

    if rfx_flag not in (0, 1):
        raise ValueError("Unsupported RFX-GLM flag: {}".format(rfx_flag))
    if serial_correlation not in (0, 1, 2):
        raise ValueError(
            "Unsupported serial-correlation flag: {}".format(serial_correlation)
        )
    if len(header["Study info"]) != nr_studies:
        raise ValueError("Study info length must equal Nr studies.")
    if len(header["Predictor info"]) != nr_predictors:
        raise ValueError("Predictor info length must equal Nr all predictors.")

    if glm_type == 0:
        spatial_shape = (header["DimZ"], header["DimX"], header["DimY"])
    elif glm_type == 1:
        r = header["Resolution multiplier (1, 2, 3 times VMR resolution)"]
        ranges = tuple(
            header[axis + "End"] - header[axis + "Start"]
            for axis in ("X", "Y", "Z")
        )
        if r <= 0 or any(size <= 0 or size % r for size in ranges):
            raise ValueError("Invalid VTC GLM bounding box or resolution.")
        dim_X, dim_Y, dim_Z = (size // r for size in ranges)
        spatial_shape = (dim_Z, dim_X, dim_Y)
    elif glm_type == 2:
        spatial_shape = (header["Nr vertices"],)
    else:
        raise ValueError("Unsupported GLM type: {}".format(glm_type))

    if any(size <= 0 for size in spatial_shape):
        raise ValueError("GLM spatial dimensions must be positive.")

    # Check all arrays before opening the output file. This also ensures that
    # a RFX map is never silently written as a standard SS/mean/AR map.
    def as_map_array(value, shape, name):
        if value is None:
            raise ValueError("{} must be provided.".format(name))
        out = np.asarray(value, dtype='<f4')
        if out.shape != shape:
            raise ValueError(
                "{} shape must be {}, got {}.".format(name, shape, out.shape)
            )
        return out

    first_map = as_map_array(data_R2, spatial_shape, "data_R2")
    if rfx_flag == 1:
        nr_rfx_betas = (
            header["Nr subjects"] * header["Nr predictors per subject"]
        )
        beta_maps = as_map_array(
            data_beta, spatial_shape + (nr_rfx_betas,), "data_beta"
        )
        if any(x is not None for x in
               (data_SS, data_SS_XiY, data_meantc, data_ARlag)):
            raise ValueError("RFX GLMs have no SS, SS_XiY, mean or AR maps.")
        nr_maps = 1 + nr_rfx_betas
        maps = [first_map] + [beta_maps[..., i]
                              for i in range(nr_rfx_betas)]
    else:
        second_map = as_map_array(data_SS, spatial_shape, "data_SS")
        beta_maps = as_map_array(
            data_beta, spatial_shape + (nr_predictors,), "data_beta"
        )
        ss_xiy_maps = as_map_array(
            data_SS_XiY, spatial_shape + (nr_predictors,), "data_SS_XiY"
        )
        mean_map = as_map_array(data_meantc, spatial_shape, "data_meantc")
        maps = [first_map, second_map]
        maps.extend(beta_maps[..., i] for i in range(nr_predictors))
        maps.extend(ss_xiy_maps[..., i] for i in range(nr_predictors))
        maps.append(mean_map)
        if serial_correlation == 1:
            maps.append(as_map_array(data_ARlag, spatial_shape, "data_ARlag"))
        elif serial_correlation == 2:
            ar_maps = as_map_array(
                data_ARlag, spatial_shape + (2,), "data_ARlag"
            )
            maps.extend([ar_maps[..., 0], ar_maps[..., 1]])
        nr_maps = 2 + 2 * nr_predictors + 1 + serial_correlation

    if "Nr maps" in header and header["Nr maps"] != nr_maps:
        raise ValueError("Nr maps in header does not match the map arrays.")

    # Prevalidate matrices and predictor RGB colors before writing so
    # malformed inputs do not leave a half-written GLM behind.
    if not rfx_flag:
        matrix_shape = (header["Nr time points"], nr_predictors)
        design_matrix = as_map_array(
            header["Design matrix"], matrix_shape, "Design matrix"
        )
        inverted_xtx = as_map_array(
            header["Inverted X'X matrix"],
            (nr_predictors, nr_predictors), "Inverted X'X matrix"
        )

    # The 'Color' field contains all four RGB triplets
    # Validate and preserve every byte, rather than zero-filling
    # or reconstructing the other nine bytes from a three-component RGB value.
    colors = []
    for pred in header["Predictor info"]:
        color = np.asarray(pred["Color"])
        if color.shape != (4, 3):
            raise ValueError("Predictor Color must have shape (4, 3).")
        if not np.issubdtype(color.dtype, np.integer) or np.any(
                color < 0) or np.any(color > 255):
            raise ValueError("Predictor color values must be bytes (0..255).")
        colors.append(color.astype(np.uint8))

    if nr_studies > 1:
        n_with_confounds = header["Nr studies with confound info"]
        if len(header["Nr confounds per study"]) != n_with_confounds:
            raise ValueError(
                "Nr confounds per study length must match its header count."
            )

    with open(filename, 'wb') as f:

        def pack(fmt, value):
            f.write(struct.pack('<' + fmt, value))

        pack('h', header["File version"])
        pack('B', glm_type)
        pack('B', rfx_flag)
        if rfx_flag:
            pack('i', header["Nr subjects"])
            pack('i', header["Nr predictors per subject"])

        pack('i', header["Nr time points"])
        pack('i', nr_predictors)
        pack('i', header["Nr confound predictors"])
        pack('i', nr_studies)
        if nr_studies > 1:
            pack('i', header["Nr studies with confound info"])
            for count in header["Nr confounds per study"]:
                pack('i', count)

        pack('B', header["Separate predictors (0:no, 1:studies, 2:subjects)"])
        pack('B', header[
            "Time course normalization (1:z transform, 2:baseline z, 3:percent change)"
        ])
        pack('h', header["Resolution multiplier (1, 2, 3 times VMR resolution)"])
        pack('B', serial_correlation)
        pack('f', header["Mean serial correlation before correction"])
        pack('f', header["Mean serial correlation after correction"])

        if glm_type == 0:
            for axis in ("DimX", "DimY", "DimZ"):
                pack('h', header[axis])
        elif glm_type == 1:
            for axis in ("XStart", "XEnd", "YStart", "YEnd", "ZStart", "ZEnd"):
                pack('h', header[axis])
        else:
            pack('i', header["Nr vertices"])

        pack('B', header["Cortex-based mask (1:(grey matter) mask has been used)"])
        pack('i', header["Nr voxels in mask"])
        write_variable_length_string(f, header["Name of cortex-based mask"])

        for study in header["Study info"]:
            pack('i', study["Nr time points (volumes) in study"])
            write_variable_length_string(f, study["Name of study data"])
            if glm_type == 2:
                write_variable_length_string(f, study["Name of SSM"])
            write_variable_length_string(f, study["Name of SDM"])

        for predictor, color in zip(header["Predictor info"], colors):
            write_variable_length_string(f, predictor["Name (internal)"])
            write_variable_length_string(f, predictor["Name (custom)"])
            # Write all four triplets in their original order.
            for rgb in color:
                write_RGB_bytes(f, rgb)

        if not rfx_flag:
            design_matrix.tofile(f)
            inverted_xtx.tofile(f)

        # NOTE[Judith]: Invert the reader's map transformation. For surface
        # data, each map is a flat vertex vector. For volumes, undo
        # reversal and axis permutation before writing map-major (Z,Y,X).
        for array in maps:
            if glm_type == 2:
                np.asarray(array, dtype='<f4').tofile(f)
            else:
                np.asarray(array[::-1, ::-1, ::-1].transpose(0, 2, 1),
                           dtype='<f4').tofile(f)
