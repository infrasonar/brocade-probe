from libprobe.probe import Probe
from lib.check.brocade import check_brocade
from lib.check.fcfxport import check_fcfxport
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'brocade': check_brocade,
        'fcfxport': check_fcfxport,
    }

    probe = Probe("brocade", version, checks)

    probe.start()
