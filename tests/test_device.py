from bussdcc.testing import RuntimeHarness
from bussdcc.device import Device
from bussdcc import message


class FakeDevice(Device[None]):
    kind = "fake"

    def connect(self):
        pass

    def disconnect(self):
        pass


def test_device_lifecycle():
    h = RuntimeHarness()

    device = FakeDevice(id="d1", config=None)
    h.runtime.devices.attach(device)

    with h:
        pass

    assert h.last(message.DeviceOnline).device == "d1"
