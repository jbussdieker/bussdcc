from bussdcc.testing import RuntimeHarness
from bussdcc.service import Service
from bussdcc import message


class Heartbeat(Service):
    name = "heartbeat"
    interval = 10

    def tick(self, ctx):
        ctx.emit(message.SystemSignal(signal=0, action="heartbeat"))

def test_service_ticks():
    h = RuntimeHarness(fake_time=True)

    h.runtime.services.register(Heartbeat())

    with h:
        h.clock.advance(10)

    assert len(h.of_type(message.SystemSignal)) == 1
