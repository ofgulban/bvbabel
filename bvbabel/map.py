"""Read, write, create BrainVoyager MAP file format."""

import struct
import numpy as np
from bvbabel.utils import read_variable_length_string
from bvbabel.utils import write_variable_length_string


# =============================================================================
def read_map(filename):
    """Read BrainVoyager MAP file. Version 3

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        MAP header.
    data : numpy.array
        Image data with dimensions [DimX, DimY, NrOfSlices]. For
        cross-correlation maps, the float is split into integer/lag
        and fractional/correlation components and returned as
        [DimX, DimY, NrOfSlices, 2].

    """
    header = dict()
    with open(filename, 'rb') as f:
        # ---------------------------------------------------------------------
        # MAP header
        # ---------------------------------------------------------------------

        # Expected binary data: short int (2 bytes)
        #
        # The first MAP value combines map type and number of slices.
        #   0     + NrOfSlices : t-values / percent-signal-change / other
        #   10000 + NrOfSlices : correlation values
        #   20000 + NrOfSlices : cross-correlation values
        #   30000 + NrOfSlices : F-values
        data, = struct.unpack('<h', f.read(2))

        if 30000 <= data:
            header["MapType"] = 'F-values'
            header["MapTypeCode"] = 30000
            header["NrOfSlices"] = int(data - 30000)
        elif 20000 <= data:
            header["MapType"] = 'crosscorrelation'
            header["MapTypeCode"] = 20000
            header["NrOfSlices"] = int(data - 20000)
        elif 10000 <= data:
            header["MapType"] = 'correlation'
            header["MapTypeCode"] = 10000
            header["NrOfSlices"] = int(data - 10000)
        elif data >= 0:
            # Type code 0 is ambiguous in the MAP file itself. BrainVoyager
            # uses it for t-maps and percent-signal-change map.
            # Keep the bvbabel default label 
            header["MapType"] = 't-values'
            header["MapTypeCode"] = 0
            header["NrOfSlices"] = int(data)
        else:
            raise ValueError(
                "Invalid MAP NrOfSlices/MapType value: "
                f"{data}."
            )

        data, = struct.unpack('<h', f.read(2))
        header["NrOfMaps"] = int(data)
        data, = struct.unpack('<h', f.read(2))
        header["DimY"] = int(data)
        data, = struct.unpack('<h', f.read(2))
        header["DimX"] = int(data)
        data, = struct.unpack('<h', f.read(2))
        header["ClusterSize"] = int(data)

        # Expected binary data: float (4 bytes)
        data, = struct.unpack('<f', f.read(4))
        header["Min"] = data  # Statistical threshold, critical value
        data, = struct.unpack('<f', f.read(4))
        header["Max"] = data  # Statistical threshold, max value

        # Expected binary data: short int (2 bytes)
        if header["MapType"] == 'crosscorrelation':
            data, = struct.unpack('<h', f.read(2))
            header["NrOfLags"] = int(data)

        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2))
        header["Reserved"] = int(data)
        if header["Reserved"] != 9999:
            raise ValueError(
                "Invalid MAP reserved field: expected 9999, "
                f"got {header['Reserved']}."
            )

        # Expected binary data: short int (2 bytes)
        data, = struct.unpack('<h', f.read(2))
        header["FileVersion"] = int(data)

        if header["FileVersion"] == 3:
            # Expected binary data: int (4 bytes)
            data, = struct.unpack('<i', f.read(4))
            header["df1"] = int(data)
            data, = struct.unpack('<i', f.read(4))
            header["df2"] = int(data)
        elif header["FileVersion"] != 2:
            raise ValueError(
                "Unsupported MAP file version: "
                f"{header['FileVersion']}. Expected version 2 or 3."
            )

        # Expected binary data: variable-length string
        data = read_variable_length_string(f)
        header["RTCName"] = data

        if header["NrOfMaps"] != header["NrOfSlices"]:
            raise ValueError(
                "Invalid MAP header: NrOfMaps must equal NrOfSlices "
                f"({header['NrOfMaps']} != {header['NrOfSlices']})."
            )

        # ---------------------------------------------------------------------
        # Read MAP image data
        # ---------------------------------------------------------------------
        data_img = []
        nr_values = header['DimY'] * header['DimX']

        for s in range(header['NrOfMaps']):
            # Each slice is preceded by its zero-based slice index.
            data, = struct.unpack('<h', f.read(2))
            if int(data) != s:
                raise ValueError(
                    "Invalid MAP slice index: "
                    f"expected {s}, got {int(data)}."
                )

            slice_data = np.fromfile(f, dtype='<f4', count=nr_values)
            if slice_data.size != nr_values:
                raise EOFError(
                    "Unexpected end of MAP file while reading "
                    f"slice {s}."
                )

            # MAP stores rows as [DimY, DimX]. bvbabel exposes image arrays as
            # [DimX, DimY, NrOfSlices].
            slice_data = np.reshape(
                slice_data, (header['DimY'], header['DimX'])
            ).T
            data_img.append(slice_data[:, :, None])

    data_img = np.concatenate(data_img, axis=2)
    data_img = data_img[::-1, ::-1, :]  # Flip BrainVoyager axes

    # -------------------------------------------------------------------------
    # For cross-correlation maps: split the packed float into its integer (lag)
    # and fractional (correlation) parts.
    if header["MapType"] == 'crosscorrelation':
        data_lag = np.floor(data_img)
        data_corr = data_img % 1
        data_img = np.stack((data_lag, data_corr), axis=3)
    # -------------------------------------------------------------------------

    return header, data_img


# =============================================================================
def write_map(filename, header, data_img):
    """Write BrainVoyager MAP file.

    Parameters
    ----------
    filename : string
        Path to file.
    header : dictionary
        MAP header. 
    data_img : numpy.array
        Image data with dimensions [DimX, DimY, NrOfSlices].

    """
    data_img = np.asarray(data_img)

    map_type = header.get("MapType", "t-values")
    if map_type == 'correlation':
        map_type_code = 10000
    elif map_type in ('crosscorrelation', 'cross-correlation'):
        map_type_code = 20000
    elif map_type in ('F-values', 'f-values'):
        map_type_code = 30000
    elif map_type in (
        't-values',
        'percent-signal-change',
        'percent signal change',
        'percent-signal-change-values',
    ):
        # Type code 0 is also used by the supplied percent-signal-change map.
        map_type_code = 0
    else:
        raise ValueError(f"Unsupported MAP MapType: {map_type!r}.")

    # cross-correlation map is presented as two maps
    # and packed again by summing the integer and fractional components.
    if map_type_code == 20000:
        if data_img.ndim != 4 or data_img.shape[3] != 2:
            raise ValueError(
                "Cross-correlation MAP data must have dimensions "
                "[DimX, DimY, NrOfSlices, 2]."
            )
        data_img = data_img[:, :, :, 0] + data_img[:, :, :, 1]
    elif data_img.ndim != 3:
        raise ValueError(
            "MAP data must be a 3D array with dimensions "
            "[DimX, DimY, NrOfSlices]."
        )

    dim_x, dim_y, nr_slices = data_img.shape

    # Keep the file dimensions consistent
    for key, expected in (
        ("DimX", dim_x),
        ("DimY", dim_y),
        ("NrOfSlices", nr_slices),
        ("NrOfMaps", nr_slices),
    ):
        if key in header and int(header[key]) != expected:
            raise ValueError(
                f"MAP header {key} ({header[key]}) does not match "
                f"the data ({expected})."
            )

    encoded_slices = map_type_code + nr_slices
    if encoded_slices > 32767:
        raise ValueError(
            "MAP NrOfSlices/MapType value exceeds the signed 16-bit range."
        )

    file_version = int(header.get("FileVersion", 3))
    if file_version not in (2, 3):
        raise ValueError(
            f"Unsupported MAP file version: {file_version}. "
            "Expected version 2 or 3."
        )

    reserved = int(header.get("Reserved", 9999))
    if reserved != 9999:
        raise ValueError(
            f"MAP reserved field must be 9999, got {reserved}."
        )

    with open(filename, 'wb') as f:
        # ---------------------------------------------------------------------
        # MAP header
        # ---------------------------------------------------------------------

        # Expected binary data: short int (2 bytes)
        f.write(struct.pack('<h', encoded_slices))
        f.write(struct.pack('<h', nr_slices))
        f.write(struct.pack('<h', dim_y))
        f.write(struct.pack('<h', dim_x))
        f.write(struct.pack('<h', int(header.get("ClusterSize", 1))))

        # Expected binary data: float (4 bytes)
        f.write(struct.pack('<f', float(header["Min"])))
        f.write(struct.pack('<f', float(header["Max"])))

        # Expected binary data: short int (2 bytes)
        if map_type_code == 20000:
            if "NrOfLags" not in header:
                raise ValueError(
                    "Cross-correlation MAP files require header['NrOfLags']."
                )
            f.write(struct.pack('<h', int(header["NrOfLags"])))

        # Expected binary data: short int (2 bytes)
        f.write(struct.pack('<h', reserved))
        f.write(struct.pack('<h', file_version))

        if file_version == 3:
            # Expected binary data: int (4 bytes)
            f.write(struct.pack('<i', int(header.get("df1", 0))))
            f.write(struct.pack('<i', int(header.get("df2", 0))))

        # Expected binary data: variable-length string
        write_variable_length_string(f, header.get("RTCName", "<untitled>"))

        # ---------------------------------------------------------------------
        # Write MAP image data
        # ---------------------------------------------------------------------
        data_img = data_img[::-1, ::-1, :]  # Restore BrainVoyager axes

        for s in range(nr_slices):
            # Each slice is preceded by its zero-based slice index.
            f.write(struct.pack('<h', s))

            # bvbabel data are [DimX, DimY]; MAP stores [DimY, DimX].
            slice_data = np.asarray(data_img[:, :, s].T, dtype='<f4')
            slice_data.tofile(f)
