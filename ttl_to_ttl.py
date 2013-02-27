import sys

import matplotlib
matplotlib.rcParams['backend'] = 'Qt4Agg'
matplotlib.rcParams['backend.qt4'] = 'PySide'

from matplotlib import pyplot
from PySide import QtGui

from mworks.conduit import IPCAccumClientConduit


times = []


def report_elapsed_times(events):
    global times
    if events:
        times += [e.data for e in events]
        pyplot.cla()
        pyplot.hist(times, bins=100)
        pyplot.title('TTL to TLL (%d trials)' % len(times))
        pyplot.xlabel('Elapsed time (ms)')
        pyplot.draw()


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
                                    ['elapsed_time'])
    conduit.initialize()

    try:
        conduit.register_bundle_callback(report_elapsed_times)
        pyplot.ion()
        pyplot.cla()
        QtGui.QApplication.instance().exec_()
    finally:
        conduit.finalize()


if __name__ == '__main__':
    main()
