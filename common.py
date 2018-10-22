import Queue
import sys
sys.path.insert(0, '/Library/Application Support/MWorks/Scripting/Python')

from matplotlib import pyplot

from mworks.conduit import IPCAccumClientConduit


class Conduit(IPCAccumClientConduit):

    update_interval = 0.5  # seconds

    def __init__(self, resource_name, event_handler, event_names):
        super(IPCAccumClientConduit, self).__init__(resource_name,
                                                    'start',
                                                    'stop',
                                                    event_names)
        self.event_handler = event_handler
        self._queue = Queue.Queue()

    def _post_events(self, events):
        if events:
            self._queue.put(events)

    def run(self):
        self.initialize()
        try:
            self.register_bundle_callback(self._post_events)

            pyplot.cla()
            pyplot.draw()
            canvas = pyplot.gcf().canvas
            canvas.manager.show()

            while True:
                try:
                    events = self._queue.get(timeout=self.update_interval)
                    self.event_handler(self, events)
                except Queue.Empty:
                    pass
                # Run the event loop, so that the plot is visible
                canvas.start_event_loop(timeout=self.update_interval)
        finally:
            self.finalize()

    @classmethod
    def main(cls, event_handler, event_names):
        if len(sys.argv) > 1:
            # Client-side conduit: resource name is a script argument
            resource_name = sys.argv[1]
        else:
            # Server-side conduit: resource name is set in the experiment
            resource_name = 'server_conduit'

        cls(resource_name, event_handler, event_names).run()
