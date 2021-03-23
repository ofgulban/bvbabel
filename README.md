# bvbabel
A lightweight read & write utility for BrainVoyager file formats. bvbabel is a spiritual successor of [Neuroelf](https://neuroelf.net/)'s xff function and the currently unmerged Nibabel BrainVoyager I/O [pull request](https://github.com/nipy/nibabel/pull/216).

| File format | Read | Write |
| ------------|------|-------|
| [VMR](https://support.brainvoyager.com/brainvoyager/automation-development/84-file-formats/343-developer-guide-2-6-the-format-of-vmr-files)| Yes  | No    |
| [VTC](https://support.brainvoyager.com/brainvoyager/automation-development/84-file-formats/348-users-guide-2-3-the-format-of-vtc-files)| Yes   | No    |
| [VMP](https://support.brainvoyager.com/brainvoyager/automation-development/84-file-formats/353-users-guide-2-3-the-format-of-nr-vmp-files) | No   | No    |
| [FMR](https://support.brainvoyager.com/brainvoyager/automation-development/84-file-formats/340-developer-guide-2-6-the-format-of-fmr-files) | No   | No    |

## Dependencies

| Package                               | Tested version |
|---------------------------------------|----------------|
| [Python 3](https://www.python.org/)   | 3.7.8          |
| [NumPy](http://www.numpy.org/)        | 1.17.2         |
| [Nibabel*](https://nipy.org/nibabel/) | 2.2.1          |

*Nibabel is only needed for nifti exports.

## BrainVoyager documentation

- [Overview](https://support.brainvoyager.com/brainvoyager/automation-development/84-file-formats/339-developer-guide-2-6-file-formats-overview)
- [General overview](https://support.brainvoyager.com/brainvoyager/automation-development/84-file-formats/38-general-overview-of-file-formats)
- [File format categories](https://support.brainvoyager.com/brainvoyager/automation-development/84-file-formats/41-file-formats-categorised)

## License
This project is licensed under MIT.

## Acknowledgments
Development and maintenance of this project is actively supported by [Brain Innovation](https://www.brainvoyager.com/) as the main developer ([Omer Faruk Gulban](https://github.com/ofgulban)) works there.
