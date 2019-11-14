import sys

from matplotlib import pyplot
import numpy

from mworks.data import MWKFile


MISSING_DATA = -32768.0


def plot_position_changes(event_file, varname, color, noise_thresh=0.0):
    events = [e for e in event_file.get_events(codes=[varname])
              if e.value != MISSING_DATA]

    v1 = numpy.array([e.value for e in events[:-1]])
    v2 = numpy.array([e.value for e in events[1:]])
    delta = numpy.abs(v2 - v1)
    delta /= delta.max()
    time = numpy.array([e.time for e in events[1:]]) / 1000.0

    pyplot.plot(time, delta, color=color, linestyle='-', marker='.')

    nonzeros = numpy.where(delta > noise_thresh)[0]
    onsets = []
    for index in nonzeros:
        if numpy.all(delta[index-100:index] <= noise_thresh):
            onsets.append(index)
    print(len(onsets))
    onset_times = time[onsets]
    
    pyplot.vlines(onset_times, 0, 1.1, color=color, linestyle='dashed')

    return onset_times


def main():
    with MWKFile(sys.argv[1]) as f:
        pyplot.cla()
        digital_onsets = plot_position_changes(f, 'eye_rx_digital', 'blue')
        analog_onsets = plot_position_changes(f, 'eye_rx_analog', 'red', 0.05)
        assert len(digital_onsets) == len(analog_onsets)
        title = ('EyeLink 1000 digital vs. analog (%d saccades)' %
                 len(digital_onsets))
        pyplot.title(title)
        pyplot.xlabel('Elapsed time (ms)')
        pyplot.ylabel('Eye position change (normalized)')
        pyplot.show()
        
        pyplot.cla()
        pyplot.hist(analog_onsets-digital_onsets, bins=100)
        pyplot.title(title)
        pyplot.xlabel('Analog saccade-onset detection lag (ms)')
        pyplot.show()


if __name__ == '__main__':
    main()
