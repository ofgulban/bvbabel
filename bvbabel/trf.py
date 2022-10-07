""" Read and write BrainVoyager TRF file format."""

import os
import numpy as np

"""
The format of TRF files

Parameter: description of possible values

"FileVersion:" 8 (current version)
"DataFormat:" "Matrix"
            4x4 float values (16 decimals)                
"TransformationType:" 1-5 (int)
                1. rigid body: 9 parameters. Order of parameters: 3 for scaling, 3 for rotation in degrees and 3 for translation
                2. affine transformation: 16 parameters (4 x 4 matrix)
                3. MNI (only with adjusted bounding box?)
                4. Talairach transformation
                5. "Untal" transformation: Talairach coordinate system to BrainVoyager coordinate system
"CoordinateSystem:" 0-1
"\n"
"NSlicesFMRVMR:
"SlThickFMRVMR:
"SlGapFMRVMR:
"CreateFMR3DMethod:
"AlignmentStep:" 1: initial alignment 2: fine alignment
"ExtraVMRTransf:" 0-1
"SourceFile:" "C:/path/to/file.fmr"
"TargetFile:" "C:/path/to/file.vmr"

"""
# =============================================================================


def read_trf(filename):
    """Read Brainvoyager TRF file

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : metadata; dictionary
    data : dictionary; one dictionary with entry "Matrix" containing a transformation matrix (NumPy 4x4 array)
        and possibly a matrix with key "ExtraVMRTransf" (NumPy 4x4 array)

    Description
    -------
    An TRF file consists of the following header fields: see above.

    Current TRF file version: 8
    """

    with open(filename, 'r') as f:
        lines = [r for r in (line.strip() for line in f) if r]
        has_vmr_trf = False
        header = dict()
        for line in lines:
            content = line.split(":")
            content = [i.strip() for i in content]
            if len(content) > 1:
                if content[1].isdigit():
                    header[content[0]] = int(content[1])
                else:
                    header[content[0]] = content[1]

    for i, key in enumerate(header):
        if key.find("xScalesMNI") > -1 or key.find("yScalesMNI") > -1 or key.find("zScalesMNI") > -1:
            tmp = header[key].split(' ')
            header[key] = []
            for r, t in enumerate(tmp):
                if len(t) > 0:
                    header[key].append(float(tmp[r]))

        if key.find("ExtraVMRTransf") > -1:
            if header["ExtraVMRTransf"] > 0:
                has_vmr_trf = True

    data = dict()
    m44 = np.zeros((4, 4))
    for i, line in enumerate(lines):

        if line.find('Matrix') > -1:
            for j in range(1, 5):
                yvalues = lines[i+j].split()
                for k in range(len(yvalues)):
                    m44[j-1][k] = float(yvalues[k])
            data["Matrix"] = m44

        if line.find('ExtraVMRTransf') > -1 and has_vmr_trf:
            m44b = np.zeros((4, 4))
            for j in range(1, 5):
                yvalues = lines[i+j].split()
                for k in range(len(yvalues)):
                    m44b[j-1][k] = float(yvalues[k])
            data["ExtraVMRTransf"] = m44b

    return header, data


def write_trf(filename, header, data):
    """Write Brainvoyager TRF file.

    Parameters
    ----------
    filename : string including path to file.
    header : dictionary; metadata.
    data : dictionary with 4x4 numpy.array(s) (transformation matrix)
    """
    with open(filename, "w") as f:

        f.write("\nFileVersion:" + '\t' + str(header["FileVersion"]) + '\n\n')
        f.write('DataFormat: \tMatrix\n\n')
        for i in range(0, 4):
            f.write(' ' + "{0:.16f}".format(data["Matrix"][i][0]).rjust(20) + ' ' + "{0:.16f}".format(data["Matrix"][i][1]).rjust(20) + ' '
                    + "{0:.16f}".format(data["Matrix"][i][2]).rjust(20) + ' ' + "{0:.16f}".format(data["Matrix"][i][3]).rjust(20) + '\n')
        f.write('\nTransformationType: ' + '\t' +
                str(header["TransformationType"]) + '\n')
        f.write('CoordinateSystem: ' + '\t' +
                str(header["CoordinateSystem"]) + '\n\n')

        if header["TransformationType"] == 1:  # coregistration: initial alignment file
            f.write('NSlicesFMRVMR:' + '\t\t' +
                    str(header["NSlicesFMRVMR"]) + '\n')
            f.write('SlThickFMRVMR:' + '\t\t' +
                    str(header["SlThickFMRVMR"]) + '\n')
            f.write('SlGapFMRVMR:' + '\t\t' +
                    str(header["SlGapFMRVMR"]) + '\n')
            f.write('CreateFMR3DMethod:' + '\t' +
                    str(header["CreateFMR3DMethod"]) + '\n')
            f.write('AlignmentStep:' + '\t\t' +
                    str(header["AlignmentStep"]) + '\n\n')
            if header["FileVersion"] > 4:
                f.write('ExtraVMRTransf:' + '\t\t' +
                        str(header["ExtraVMRTransf"]) + '\n\n')
                if header["ExtraVMRTransf"] > 0:
                    for i in range(0, 4):
                        f.write(' ' + "{0:.16f}".format(data["ExtraVMRTransf"][i][0]).rjust(20) + ' ' + "{0:.16f}".format(data["ExtraVMRTransf"][i][1]).rjust(20) + ' '
                                + "{0:.16f}".format(data["ExtraVMRTransf"][i][2]).rjust(20) + ' ' + "{0:.16f}".format(data["ExtraVMRTransf"][i][3]).rjust(20) + '\n')
                    f.write('\n')
            if header["AlignmentStep"] == 1 and header["FileVersion"] > 5:  # initial alignment
                f.write('ToVMRFramingCube:' + '\t' +
                        str(header["ToVMRFramingCube"]) + '\n')
                f.write('ToVMRVoxelRes:' + '\t\t' +
                        str(header["ToVMRVoxelRes"]) + '\n\n')
        elif header["TransformationType"] == 3:  # *_cMNI_adjBBX.trf
            for scale in [("xScalesMNI", "\n"), ("yScalesMNI", "\n"), ("zScalesMNI", "\n\n")]:
                f.write(scale[0] + ':' + '\t\t' + "{:>10.5f}".format(header[scale[0]][0]) + '\t' + "{:>10.5f}".format(header[scale[0]][1]) + scale[1])
        elif header["TransformationType"] == 4:  # TAL
            pass  # no example data available
        elif header["TransformationType"] == 5:  # UNTAL
            pass  # no example data available
        f.write('SourceFile:' + '\t\t' + str(header["SourceFile"]) + '\n')
        f.write('TargetFile:' + '\t\t' + str(header["TargetFile"]) + '\n\n')
        # only for ACPC, not for MNI; fields present at least since 2016
        if header["TransformationType"] == 2 and filename.find("ACPC") > -1:
            f.write('ACPCVMRFramingCube:' + '\t' +
                    str(header["ACPCVMRFramingCube"]) + '\n')
            f.write('ACPCVMRVoxelRes:' + '\t' +
                    str(header["ACPCVMRVoxelRes"]) + '\n\n')
        f.close()  # officially not required
