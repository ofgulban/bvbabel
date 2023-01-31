"""Test bvbabel file read write functions.

NOTES
-----
In the command line, navigate to bvbabel directory and run `pytest`.

"""

import os
import pytest
import numpy as np
import bvbabel
import pytest
import gzip
import shutil

SOURCE = "/home/faruk/Git/bvbabel/test_data/sub-test01_fileversion-2.vmr.gz"

DIRNAME = os.path.dirname(SOURCE)
BASENAME, EXT, _ = SOURCE.split(os.extsep, 2)
BASENAME = os.path.basename(BASENAME)
OUTPUTDIR = os.path.join(DIRNAME, "temp_tests")
INPUT1 = os.path.join(OUTPUTDIR, f"{BASENAME}.{EXT}")
INPUT2 = os.path.join(OUTPUTDIR, f"{BASENAME}_bvbabel.{EXT}")

# =============================================================================
# Output directory
if not os.path.exists(OUTPUTDIR):
    os.makedirs(OUTPUTDIR)
print("  Output directory: {}\n".format(OUTPUTDIR))

# -----------------------------------------------------------------------------
# Unzip
with gzip.open(SOURCE, 'rb') as f_in:
    with open(INPUT1, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

def test_vmr_header_roundtrip():
    """Test VMR header read and write."""
    header1, data1 = bvbabel.vmr.read_vmr(INPUT1)
    bvbabel.vmr.write_vmr(INPUT2, header1, data1)
    header2, data2 = bvbabel.vmr.read_vmr(INPUT2)
    assert header1 == header2

def test_vmr_data_roundtrip():
    """Test VMR data read and write."""
    header1, data1 = bvbabel.vmr.read_vmr(INPUT1)
    bvbabel.vmr.write_vmr(INPUT2, header1, data1)
    header2, data2 = bvbabel.vmr.read_vmr(INPUT2)
    assert np.array_equal(data1, data2)

# Cleanup
os.remove(INPUT1)
os.remove(INPUT2)
