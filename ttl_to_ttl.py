from matplotlib import pyplot


times = []


def report_elapsed_times(conduit, events):
    global times
    times += [e.data for e in events]
    pyplot.cla()
    pyplot.hist(times, bins=100)
    pyplot.title('TTL to TLL (%d trials)' % len(times))
    pyplot.xlabel('Elapsed time (ms)')
    pyplot.draw()


if __name__ == '__main__':
    from common import Conduit
    Conduit.main(report_elapsed_times, ['elapsed_time'])
