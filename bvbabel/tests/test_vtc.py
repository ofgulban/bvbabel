"""Test bvbabel VTC functions."""

import pytest
import numpy as np
import bvbabel


# =============================================================================
# TODO[Faruk]: Add read write functions into these tests.
def test_VTC_rearrange_axes_True():
    """Test VTC rearrange_axes option."""
    header, data = bvbabel.vtc.create_vtc(rearrange_data_axes=True)
    header_dims = np.zeros(4, dtype=int)
    header_dims[0] = header["XEnd"] - header["XStart"]
    header_dims[1] = header["YEnd"] - header["YStart"]
    header_dims[2] = header["ZEnd"] - header["ZStart"]
    header_dims[3] = header["Nr time points"]

    data_dims = np.array(data.shape)
    assert np.array_equal(header_dims, data_dims)


# TODO[Faruk]: Add read write functions into these tests.
def test_VTC_rearrange_axes_False():
    """Test VTC rearrange_axes option."""
    header, data = bvbabel.vtc.create_vtc(rearrange_data_axes=False)
    header_dims = np.zeros(4, dtype=int)
    header_dims[0] = header["XEnd"] - header["XStart"]
    header_dims[1] = header["YEnd"] - header["YStart"]
    header_dims[2] = header["ZEnd"] - header["ZStart"]
    header_dims[3] = header["Nr time points"]

    data_dims = np.array(data.shape)
    assert np.array_equal(header_dims[[2, 1, 0, 3]], data_dims)
