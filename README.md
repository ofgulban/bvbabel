# bvbabel
A lightweight Python library for reading & writing [BrainVoyager](https://www.brainvoyager.com/products/brainvoyager.html) file formats.

`bvbabel` is a spiritual successor of [Neuroelf](https://neuroelf.net/)'s `xff` function and the currently unmerged Nibabel BrainVoyager I/O [pull request](https://github.com/nipy/nibabel/pull/216).


### File format support overview

| File format | Read | Write | Priority |
| ------------|------|-------|----------|
| VMR         | Yes  | No    | High     |
| VTC         | Yes  | No    | High     |
| VMP         | Yes  | No    | High     |
| SRF         | No   | No    | High     |
| SMP         | No   | No    | High     |
| FMR & STC   | No   | No    | Medium   |
| VOI         | No   | No    | Low      |
| POI         | No   | No    | Low      |
| MTC         | No   | No    | Low      |
| GLM         | No   | No    | Low      |

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
