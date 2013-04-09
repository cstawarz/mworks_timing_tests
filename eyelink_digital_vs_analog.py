import sys

import matplotlib
matplotlib.rcParams['backend'] = 'Qt4Agg'
matplotlib.rcParams['backend.qt4'] = 'PySide'

from matplotlib import pyplot
import numpy

from mworks.data import MWKFile


MISSING_DATA = -32768.0


def plot_position_changes(event_file, varname, color):
    events = [e for e in event_file.get_events(codes=[varname])
              if (e.value != 0.0) and (e.value != MISSING_DATA)]

    v1 = numpy.array([e.value for e in events[:-1]])
    v2 = numpy.array([e.value for e in events[1:]])
    delta = numpy.abs(v2 - v1)
    delta /= delta.max()
    
    time = numpy.array([e.time for e in events[1:]]) / 1000.0

    pyplot.plot(time, delta, color)


def main():
    with MWKFile(sys.argv[1]) as f:
        pyplot.cla()
        plot_position_changes(f, 'eye_h_digital', 'blue')
        plot_position_changes(f, 'eye_h_analog', 'red')
        #pyplot.title('Eye-in-window to TLL (%d trials)' % len(times))
        pyplot.xlabel('Elapsed time (ms)')
        pyplot.show()


if __name__ == '__main__':
    main()
