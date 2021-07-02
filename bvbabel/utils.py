"""Utility functions."""
import struct
import numpy as np


def check_extension():
    """Check whether the file extension is proper before reading any bytes."""
    print("TODO")


def read_variable_length_string(f):
    r"""Read Brainvoyager variable length strings terminate with b'\x00'."""
    text = ""
    data, = struct.unpack('<s', f.read(1))
    while data != b'\x00':
        text += data.decode("utf-8")
        data = f.read(1)
    return text


def write_variable_length_string(f, in_string):
    r"""Write Brainvoyager variable length strings terminate with b'\x00'."""
    for i in range(len(in_string)):
        data = bytes(in_string[i], 'utf-8')
        f.write(struct.pack('<s', data))
    f.write(b'\x00')


def read_RGB_bytes(f):
    r"""Brainvoyager RGB bytes (unsigned char)."""
    RGB = np.zeros(3, dtype=np.ubyte)
    for i in range(3):
        data, = struct.unpack('<B', f.read(1))
        RGB[i] = data
    return RGB


def write_RGB_bytes(f, RGB):
    r"""Write Brainvoyager RGB bytes (unsigned char)."""
    for i in range(3):
        f.write(struct.pack('<B', RGB[i]))


def read_float_array(f, nr_floats):
    r"""Read multiple floats into 1D numpy array."""
    out_data = np.zeros(nr_floats, dtype=np.float)
    for i in range(nr_floats):
        data, = struct.unpack('<f', f.read(4))
        out_data[i] = data
    return out_data
