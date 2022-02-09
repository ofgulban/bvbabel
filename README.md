# bvbabel (work in progress)
A lightweight Python library for reading & writing [BrainVoyager](https://www.brainvoyager.com/products/brainvoyager.html) file formats.

`bvbabel` is a spiritual successor of Jochen Weber's [Neuroelf](https://neuroelf.net/)'s `xff` function and Thomas Emmerling's currently unmerged Nibabel [pull request](https://github.com/nipy/nibabel/pull/216). I have been inspired by these earlier projects, but ended up deciding to implement from scratch based on [BrainVoyager file formats documentation](https://support.brainvoyager.com/brainvoyager/automation-development/84-file-formats).


### File format support overview

| File format | Read  | Write | Create |
| ------------|-------|-------|--------|
| FMR & STC   | No    | No    | No     |
| GLM         | No    | No    | No     |
| GTC         | Yes   | Yes   | No     |
| MTC         | No    | No    | No     |
| OBJ         | No    | Yes   | No     |
| POI         | No    | No    | No     |
| PRT         | No    | No    | No     |
| SMP         | Yes   | Yes   | Yes    |
| SRF         | Yes   | No    | No     |
| SSM         | Yes   | No    | No     |
| SDM         | No    | No    | No     |
| VMP         | Yes   | Yes   | No     |
| VMR         | Yes   | Yes   | No     |
| VOI         | Yes   | No    | No     |
| VTC         | Yes   | Yes   | Yes    |

## Dependencies

| Required | Package                               | Tested version |
| ---------|---------------------------------------|----------------|
| Yes      | [Python 3](https://www.python.org/)   | 3.7.8          |
| Yes      | [NumPy](http://www.numpy.org/)        | 1.17.2         |
| No       | [NiBabel](https://nipy.org/nibabel/)  | 3.2.0          |

## Installation

1. Clone the latest release and unzip it.
2. Change directory in your command line:
```
cd /path/to/bvbabel
```
3. Install bvbabel:
```
python setup.py install
```
4. Once the installation is complete, you can have a look ant try using some of the example scripts at the [examples](examples/) folder.

## BrainVoyager documentation

- [Overview](https://support.brainvoyager.com/brainvoyager/automation-development/84-file-formats/339-developer-guide-2-6-file-formats-overview)
- [General overview](https://support.brainvoyager.com/brainvoyager/automation-development/84-file-formats/38-general-overview-of-file-formats)
- [File format categories](https://support.brainvoyager.com/brainvoyager/automation-development/84-file-formats/41-file-formats-categorised)

## License
This project is licensed under [MIT](./LICENSE).

## Acknowledgments
Development and maintenance of this project is actively supported by [Brain Innovation](https://www.brainvoyager.com/) as the main developer ([Omer Faruk Gulban](https://github.com/ofgulban)) works there.
