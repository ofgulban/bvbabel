"""For having the version."""

import bvbabel.vmr
import bvbabel.vmp
import bvbabel.vtc
import bvbabel.gtc

import pkg_resources
__version__ = pkg_resources.require("bvbabel")[0].version
