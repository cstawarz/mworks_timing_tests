from matplotlib import pyplot


def plot_times(conduit, events):
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


if __name__ == '__main__':
    from common import Conduit
    Conduit.main(plot_times, ['is_fixating', 'ttl_out'])
