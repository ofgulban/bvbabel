# bvbabel
A lightweight Python library for reading & writing [BrainVoyager](https://www.brainvoyager.com/products/brainvoyager.html) file formats.

`bvbabel` is a spiritual successor of Jochen Weber's [Neuroelf](https://neuroelf.net/)'s `xff` function and Thomas Emmerling's currently unmerged Nibabel [pull request](https://github.com/nipy/nibabel/pull/216). I have been inspired by these earlier projects, but ended up deciding to implement from scratch based on [BrainVoyager file formats documentation](https://support.brainvoyager.com/brainvoyager/automation-development/84-file-formats).


### File format support overview

| File format | Read | Write | Create |
| ------------|------|-------|--------|
| VMR         | Yes  | Yes   | No     |
| VMP         | Yes  | Yes   | No     |
| VTC         | Yes  | No    | No     |
| FMR & STC   | No   | No    | No     |
| PRT         | No   | No    | No     |
| SRF         | No   | No    | No     |
| SMP         | No   | No    | No     |
| VOI         | No   | No    | No     |
| POI         | No   | No    | No     |
| MTC         | No   | No    | No     |
| GLM         | No   | No    | No     |

## Dependencies

| Package                               | Tested version |
|---------------------------------------|----------------|
| [Python 3](https://www.python.org/)   | 3.7.8          |
| [NumPy](http://www.numpy.org/)        | 1.17.2         |

## BrainVoyager documentation

- [Overview](https://support.brainvoyager.com/brainvoyager/automation-development/84-file-formats/339-developer-guide-2-6-file-formats-overview)
- [General overview](https://support.brainvoyager.com/brainvoyager/automation-development/84-file-formats/38-general-overview-of-file-formats)
- [File format categories](https://support.brainvoyager.com/brainvoyager/automation-development/84-file-formats/41-file-formats-categorised)

## License
This project is licensed under [MIT](./LICENSE).

## Acknowledgments
Development and maintenance of this project is actively supported by [Brain Innovation](https://www.brainvoyager.com/) as the main developer ([Omer Faruk Gulban](https://github.com/ofgulban)) works there.
