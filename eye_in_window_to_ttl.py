import sys

import matplotlib
matplotlib.rcParams['backend'] = 'Qt4Agg'
matplotlib.rcParams['backend.qt4'] = 'PySide'

from matplotlib import pyplot
from PySide import QtGui

from mworks.conduit import IPCAccumClientConduit


def main():
    if len(sys.argv) > 1:
        # Client-side conduit: resource name is a script argument
        resource_name = sys.argv[1]
    else:
        # Server-side conduit: resource name is set in the experiment
        resource_name = 'server_conduit'

    conduit = IPCAccumClientConduit(resource_name,
                                    'start',
                                    'stop',
                                    ['is_fixating', 'ttl_out'])

    def plot_times(events):
        if not events:
            return

        rc = conduit.reverse_codec
        last_fixation_time = 0.0
        times = []

        for e in events:
            if e.code == rc['is_fixating']:
                if e.value:
                    last_fixation_time = e.time
            elif e.code == rc['ttl_out']:
                times.append((e.time - last_fixation_time) / 1000.0)

        pyplot.cla()
        pyplot.hist(times, bins=100)
        pyplot.title('Eye-in-window to TLL (%d trials)' % len(times))
        pyplot.xlabel('Elapsed time (ms)')
        pyplot.draw()

    conduit.initialize()
    try:
        conduit.register_bundle_callback(plot_times)
        pyplot.ion()
        pyplot.cla()
        QtGui.QApplication.instance().exec_()
    finally:
        conduit.finalize()


if __name__ == '__main__':
    main()
