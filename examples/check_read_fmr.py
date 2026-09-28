"""Simple fmr.read_fmr check using bvbabel."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import bvbabel


# ---------------------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------------------

FMR_FILE = "/path/to/data.fmr"

# X, Y, slice from BrainVoyager; slice is 1-based
VOXEL_BV = [0,0,1] # origin
VOXEL_BV = [55, 83, 24]


def bv_slice(data_3d, z):
    """
    Return one slice in BrainVoyager display orientation.
    This is mapped to the default rearrange_data_axes = True 
    when reading FMR data
    """
    return data_3d[:, ::-1, z].T


def contrast(img):
    """Robust grayscale limits."""
    values = img[img > 0]
    return np.percentile(values, [2, 98]) if values.size else (0, 1)


# ---------------------------------------------------------------------
# READ FMR
# ---------------------------------------------------------------------

header, data = bvbabel.fmr.read_fmr(FMR_FILE)

expected_shape = (
    header["ResolutionX"],
    header["ResolutionY"],
    header["NrOfSlices"],
    header["NrOfVolumes"],
)

print("Data shape:    ", data.shape)
print("Expected shape:", expected_shape)
print("Data type:     ", data.dtype)
print("Min/mean/max:  ", data.min(), data.mean(), data.max())
print("Note: BrainVoyager uses 1-based slice indexing in FMRs")

if data.shape != expected_shape:
    raise ValueError(
        f"Unexpected shape {data.shape}; expected {expected_shape}."
    )

mean_volume = data.astype(np.float32).mean(axis=3)


# ---------------------------------------------------------------------
# SELECT VOXEL
# ---------------------------------------------------------------------

x_bv, y_bv, slice_bv = VOXEL_BV

# BrainVoyager -> Python indices
x = x_bv
# this is mapped to the default rearrange_data_axes = True when
# reading FMR data (assuming BV axes: data_img[:, ::-1, :, :])
y = data.shape[1] - 1 - y_bv
z = slice_bv - 1

time_course = data[x, y, z, :]


# ---------------------------------------------------------------------
# VOXEL LOCATION + TIME COURSE 
# extract a single-voxel time course in BrainVoyager and compare with
# the displayed voxel time-course
# helps to reveal: 
# - wrong voxel-coordinate conversion 
# - wrong axis flips
# - wrong slice indexing
# - X/Y interchange
# ---------------------------------------------------------------------

img = bv_slice(mean_volume, z)
vmin, vmax = contrast(img)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].imshow(img, cmap="gray", vmin=vmin, vmax=vmax)
axes[0].add_patch(
    Rectangle(
        (x_bv - 0.5, y_bv - 0.5),
        1,
        1,
        fill=False,
        edgecolor="red",
        linewidth=1,
    )
)
axes[0].set_title(
    f"Voxel location\nX={x_bv}, Y={y_bv}, slice={slice_bv}"
)

axes[1].plot(time_course)
axes[1].set_xlabel("Volume")
axes[1].set_ylabel("Intensity")
axes[1].set_title(
    f"Voxel time course\nX={x_bv}, Y={y_bv}, slice={slice_bv}"
)

plt.tight_layout()


# ---------------------------------------------------------------------
# VOLUME-ORDER CHECK
# the same slice is presented in 2 different functional volumes
# diagnosing slice/volume issues
# ---------------------------------------------------------------------

check_slice = data.shape[2] // 2
check_slice_bv = check_slice + 1

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

# compare the same slice in different volumes
for ax, vol in zip(axes, (0, data.shape[3]-1)):
    ax.imshow(
        data[:, ::-1, check_slice, vol].T,
        cmap="gray",
    )
    ax.set_title(f"Volume {vol}, slice {check_slice_bv}")

plt.tight_layout()


# ---------------------------------------------------------------------
# MEAN-VOLUME MONTAGE
# check whether slices, their order, and the image orientation look 
# anatomically plausible
# ---------------------------------------------------------------------

n_slices = mean_volume.shape[2]
n_cols = int(np.ceil(np.sqrt(n_slices)))
n_rows = int(np.ceil(n_slices / n_cols))

fig, axes = plt.subplots(
    n_rows,
    n_cols,
    figsize=(2 * n_cols, 2 * n_rows),
)

for s, ax in enumerate(np.ravel(axes)):
    if s >= n_slices:
        ax.axis("off")
        continue

    img = bv_slice(mean_volume, s)
    vmin, vmax = contrast(img)

    ax.imshow(img, cmap="gray", vmin=vmin, vmax=vmax)
    ax.text(
        0.03,
        0.95,
        str(s + 1),
        transform=ax.transAxes,
        color="yellow",
        fontsize=9,
        va="top",
    )
    ax.axis("off")

fig.suptitle(f"Mean over {data.shape[3]} volumes")
plt.tight_layout()
plt.show()
