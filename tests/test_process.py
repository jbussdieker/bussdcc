from bussdcc.testing import RuntimeHarness
from bussdcc.process import Process
from bussdcc import message


class Recorder(Process):
    name = "rec"

    def handle_event(self, ctx, evt):
        ctx.state.set("test.hit", True)


def test_process_receives_events():
    h = RuntimeHarness()

    h.runtime.processes.register(Recorder())

    with h:
        pass

    assert h.runtime.ctx.state.get("test.hit") is True
