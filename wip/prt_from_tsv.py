"""Convert BIDS style TSV file protocols to BrainVoyager PRT format."""

import bvbabel
import numpy as np

# NOTE[Judith]: Possible trial_type column header names (as these do not seem
# to have consistent names in many event.tsv files)
trial_type_name = [
    "trial_type",
    "trial type",
    "trial name",
    "trial_name",
    "condition_type",
    "condition type",
    "condition name",
    "condition_name",
    "event_type",
    "event type",
    "event name",
    "event_name",
]

tsv_file = "C:/Users/JEck/Documents/sub-01_ses-01_task-test_run-01_events.tsv"

# =============================================================================
tsv_data = np.genfromtxt(fname=tsv_file, delimiter="\t", dtype=None, encoding=None)

col = tsv_data[0, :]

for i in range(len(col)):
    if col[i].lower().strip() == "onset":
        onsets = tsv_data[1:, i].astype("float")
    elif col[i].lower().strip() == "duration":
        durations = tsv_data[1:, i].astype("float")
    elif any(ele in col[i].lower().strip() for ele in trial_type_name):
        trial_types = tsv_data[1:, i].astype("str")

conditions = np.unique(trial_types)

prt_header = {
    "FileVersion": "2",
    "ResolutionOfTime": "msec",
    "Experiment": tsv_file.rsplit("/", 1)[-1].rsplit(".", 1)[0],
    "BackgroundColor": "0 0 0",
    "TextColor": "255 255 255",
    "TimeCourseColor": "255 255 255",
    "TimeCourseThick": "3",
    "ReferenceFuncColor": "255 255 0",
    "ReferenceFuncThick": "3",
    "NrOfConditions": str(len(conditions)),
}

prt_data = list()

trial_types_inds = trial_types.argsort()
sorted_trial_types = trial_types[trial_types_inds[::-1]]
sorted_onsets = onsets[trial_types_inds[::-1]]
sorted_durations = durations[trial_types_inds[::-1]]

colour_temp = np.linspace(225, 30, len(conditions))
inds = np.where(sorted_trial_types[:-1] != sorted_trial_types[1:])[0]
inds = np.insert(inds, 0, -1)
inds = np.append(inds, len(onsets) - 1)

for cond in range(len(conditions)):
    prt_data.append(
        {
            "NameOfCondition": str(sorted_trial_types[inds[cond] + 1]),
            "NrOfOccurances": int(inds[cond + 1] - inds[cond]),
            "Time start": np.sort(
                (sorted_onsets[inds[cond] + 1 : inds[cond + 1] + 1] * 1000).astype(int)
            ),
            "Time stop": np.sort(
                (
                    sorted_onsets[inds[cond] + 1 : inds[cond + 1] + 1] * 1000
                    + sorted_durations[inds[cond] + 1 : inds[cond + 1] + 1] * 1000
                ).astype(int)
            ),
            "Color": np.array([0, 0, int(colour_temp[cond])]),
        }
    )

bvbabel.prt.write_prt((tsv_file.rsplit(".", 1)[0] + ".prt"), prt_header, prt_data)

print("Finished.")
