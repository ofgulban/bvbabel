"""For having the version."""

import bvbabel.vmr
import bvbabel.vmp
import bvbabel.vtc
import bvbabel.gtc
import bvbabel.smp
import bvbabel.srf
import bvbabel.obj
import bvbabel.voi
import bvbabel.ssm
import bvbabel.stc
import bvbabel.fmr

import pkg_resources
__version__ = pkg_resources.require("bvbabel")[0].version
