import sys

from matplotlib import pyplot
from numpy import array, arange, concatenate


def plot_diffs(conduit, events):
    rc = conduit.reverse_codec

    def get_var(name):
        code = rc[name]
        for e in events:
            if e.code == code:
                return e.value
        raise RuntimeError('No value for variable %r' % name)

    nsamples = get_var('nsamples')
    title = get_var('title')
    interval = get_var('interval')
    start_time = get_var('start_time')

    evts = [e for e in events if e.code == rc['i']]
    times = array([e.time for e in evts])
    diffs = times - (start_time + arange(1, nsamples + 1) * interval)
    deltas = times[1:] - times[:-1]

    plot_title = '%s: %dus (%d samples)' % (title, interval, len(diffs))

    pyplot.figure(1)
    pyplot.cla()
    pyplot.hist(diffs, bins=100)
    pyplot.title(plot_title)
    pyplot.xlabel('Actual - Expected (us)')
    pyplot.draw()

    print('interval =', interval)
    print('min =', diffs.min())
    print('max =', diffs.max())
    print('mean =', diffs.mean())
    print('max-min =', diffs.max() - diffs.min())
    print()
    sys.stdout.flush()

    pyplot.figure(2)
    pyplot.cla()
    pyplot.hist(deltas, bins=100)
    pyplot.title(plot_title)
    pyplot.xlabel('Current - Previous (us)')
    pyplot.draw()


if __name__ == '__main__':
    from common import Conduit
    Conduit.main(plot_diffs,
                 ['nsamples', 'title', 'interval', 'start_time', 'i'])
