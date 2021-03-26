"""Utility functions."""
import struct
import numpy as np


def read_variable_length_string(f):
    r"""Brainvoyager variable length strings terminate with b'\x00'."""
    text = ""
    data, = struct.unpack('<s', f.read(1))
    while data != b'\x00':
        text += data.decode("utf-8")
        data = f.read(1)
    return text


def read_RGB_bytes(f):
    r"""Brainvoyager RGB bytes (unsigned char)."""
    RGB = np.zeros(3, dtype=np.ubyte)
    for i in range(3):
        data, = struct.unpack('<B', f.read(1))
        RGB[i] = data
    return RGB


def read_float_array(f, nr_floats):
    r"""Read multiple floats into 1D numpy array."""
    out_data = np.zeros(nr_floats, dtype=np.float)
    for i in range(nr_floats):
        data, = struct.unpack('<f', f.read(4))
        out_data[i] = data
    return out_data
