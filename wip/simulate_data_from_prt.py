"""Simulate timeseries dat from a protocol file."""

import bvbabel as bv
import numpy as np
import matplotlib.pyplot as plt


PRT = "/home/faruk/Git/bvbabel/test_data/sub-test05.prt"

REACTIVITY = 1/5
BASELINE = 100.

# =============================================================================

prt = bv.prt.read_prt(PRT)


def activity(intercept, slope, t):
    return t * slope + intercept

# -----------------------------------------------------------------------------
# Simulate signal goes up for condition A
timeseries = np.full(300, BASELINE)
starts = prt[1][1]["Time start"].astype(int)
ends = prt[1][1]["Time stop"].astype(int)
for i, j in enumerate(starts):
    end = ends[i]
    nr_timepoints = end-j
    for k in range(0, nr_timepoints):
        signal = activity(BASELINE, REACTIVITY, k)
        print(signal)
        timeseries[j+k] = signal
    for k in range(0, nr_timepoints):
        timeseries[end+k] = activity(timeseries[end-1], -REACTIVITY, k)

plt.plot(timeseries)

# -----------------------------------------------------------------------------
# Simulate signal goes up for condition B
timeseries = np.full(300, BASELINE)
starts = prt[1][2]["Time start"].astype(int)
ends = prt[1][2]["Time stop"].astype(int)
for i, j in enumerate(starts):
    end = ends[i]
    nr_timepoints = end-j
    for k in range(0, nr_timepoints):
        signal = activity(BASELINE, REACTIVITY, k)
        print(signal)
        timeseries[j+k] = signal
    for k in range(0, nr_timepoints):
        timeseries[end+k] = activity(timeseries[end-1], -REACTIVITY, k)

plt.plot(timeseries)
