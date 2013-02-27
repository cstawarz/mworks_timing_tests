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

    conduit = IPCAccumClientConduit(
        resource_name,
        'start',
        'stop',
        ['photodiode_signal', 'vsync_signal', '#stimDisplayUpdate',
        '#announceMessage'],
        )

    def plot_events(events):
        if not events:
            return

        rc = conduit.reverse_codec
        t0 = min(e.time for e in events)

        ps = [e for e in events if e.code == rc['photodiode_signal']]
        ps_times = [(e.time - t0)/1000.0 for e in ps]
        ps_values = [e.value for e in ps]

        vs_times = [(e.time - t0)/1000.0 for e in events
                    if (e.code == rc['vsync_signal']) and (e.value == 1)]

        sdu_times = [(e.time - t0)/1000.0 for e in events if
                     (e.code == rc['#stimDisplayUpdate']) and
                     isinstance(e.value, list) and
                     isinstance(e.value[0], dict) and
                     (e.value[0]['name'] == 'frame_list') and
                     isinstance(e.value[0]['current_stimulus'], dict) and
                     (e.value[0]['current_stimulus']['name'] == 'white_screen')]

        skip_times = [(e.time - t0)/1000.0 for e in events if
                      (e.code == rc['#announceMessage']) and
                      isinstance(e.data, dict) and
                      e.data['message'].startswith('WARNING: Skipped ') and
                      e.data['message'].endswith(' display refresh cycles')]

        pyplot.cla()
        pyplot.plot(ps_times, ps_values)

        y_min, y_max = pyplot.gca().get_ylim()
        pyplot.vlines(vs_times, y_min, y_max)
        pyplot.vlines(sdu_times, y_min, y_max, color='red')
        if skip_times:
            pyplot.vlines(skip_times, y_min, y_max, color='green')

        pyplot.title('Display update timing (CRT @ 60Hz)')
        pyplot.xlabel('Elapsed time (ms)')
        pyplot.ylabel('Photodiode voltage')
        
        pyplot.draw()

    conduit.initialize()
    try:
        conduit.register_bundle_callback(plot_events)
        pyplot.ion()
        pyplot.cla()
        QtGui.QApplication.instance().exec_()
    finally:
        conduit.finalize()


if __name__ == '__main__':
    main()
