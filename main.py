from libprobe.probe import Probe
from lib.check.brocade import CheckBrocade
from lib.check.fcfxport import CheckFcFxPort
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckBrocade,
        CheckFcFxPort,
    )

    probe = Probe("brocade", version, checks)

    probe.start()
