from bussdcc.testing import RuntimeHarness
from bussdcc import message


def test_runtime_boot():
    with RuntimeHarness() as h:
        pass

    h.assert_emitted(message.RuntimeBooted)
    h.assert_emitted(message.RuntimeShutdown)
