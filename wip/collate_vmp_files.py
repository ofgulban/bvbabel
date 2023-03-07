"""Collate VMP files."""

import os
import bvbabel
import numpy as np
import pprint


FILES = [
    "/path/to/sub-control03_run-01_facefix_beta.vmp",
    "/path/to/sub-control03_run-02_facefix_beta.vmp",
    "/path/to/sub-control03_run-03_facefix_beta.vmp",
    "/path/to/sub-control03_run-04_facefix_beta.vmp",
]

SUFFIX = "collated_bvbabel"

# =============================================================================
for i in range(len(FILES)):
    # Load main vmr
    header_main, data_main = bvbabel.vmp.read_vmp(FILES[i])

    # Add subject identifier to the map name
    basename = FILES[i].split(os.extsep, 1)[0]
    filename = basename.split(os.sep)[-1]
    mapname_main = header_main["Map"][0]["MapName"]
    header_main["Map"][0]["MapName"] = f"{filename}: {mapname_main}"

    for j in range(len(FILES)):
        if j == i:
            pass
        else:
            # Load additional vmr
            header_temp, data_temp = bvbabel.vmp.read_vmp(FILES[j])

            # Add subject identifier to the map name
            basename_temp = FILES[j].split(os.extsep, 1)[0]
            filename_temp = basename_temp.split(os.sep)[-1]
            mapname = header_temp["Map"][0]["MapName"]
            header_temp["Map"][0]["MapName"] = f"{filename_temp}: {mapname}"

            # Append new VMP map from another subject
            header_main["NrOfSubMaps"] += 1
            header_main["Map"].append(header_temp["Map"][0])
            data_main = np.concatenate([data_main, data_temp], axis=3)

    # Write VMP
    outname = f"{basename}_{SUFFIX}.vmp"
    bvbabel.vmp.write_vmp(outname, header_main, data_main)

print("Finished.")
