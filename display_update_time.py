from matplotlib import pyplot


def plot_events(conduit, events):
    rc = conduit.reverse_codec
    t0 = min(e.time for e in events)

    ps = [e for e in events if e.code == rc['photodiode_signal']]
    ps_times = [(e.time - t0)/1000.0 for e in ps]
    ps_values = [e.value for e in ps]

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
    pyplot.vlines(sdu_times, y_min, y_max, color='red')
    if skip_times:
        pyplot.vlines(skip_times, y_min, y_max, color='green')

    pyplot.title('Display update timing (LCD @ 60Hz)')
    pyplot.xlabel('Elapsed time (ms)')
    pyplot.ylabel('Photodiode voltage')
    
    pyplot.draw()


if __name__ == '__main__':
    from common import Conduit
    Conduit.main(plot_events, ['photodiode_signal',
                               '#stimDisplayUpdate',
                               '#announceMessage'])
