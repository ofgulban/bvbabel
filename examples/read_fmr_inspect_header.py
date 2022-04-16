"""Read BrainVoyager FMR file format."""

import time
ssimport bvbabel

FILE = "/home/faruk/Documents/test_bvbabel/fmr/nifti_converted.fmr"

# =============================================================================
start = time.time()
header, data = bvbabel.fmr.read_fmr(FILE)
end = time.time()

# Print header information
print("\nFMR information")
for key, value in header.items():
    print("  ", key, ":", value)

print("\nPosition information")
for key, value in header["Position information"].items():
    print("  ", key, ":", value)

print("\nTransformation information")
for key, value in header["Transformation information"].items():
    print("  ", key, ":", value)

print("\nMultiband information")
for key, value in header["Multiband information"].items():
    print("  ", key, ":", value)

print("STC data dimensions: {} {} {} {} [x, y, slices, time]".format(
      header["ResolutionX"], header["ResolutionY"], header["NrOfSlices"],
      header["NrOfVolumes"])
      )

print("FMR and STC read in: {:.2f} seconds".format(end - start))

print("Finished.")
