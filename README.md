# BussDCC

**bussdcc** (Bussdieker Durable Cybernetic Core) is a **minimal, strongly-typed cybernetic runtime for Python**.

It provides a resilient core for building systems that coordinate **devices**, **processes**, and **services** through **explicit lifecycles**, **event-driven communication**, and **strict typing**.

The project is intentionally **lightweight**: it defines *contracts and flow*, not application policies.

---

## Design Philosophy

bussdcc is built around a few guiding principles:

* **Cybernetics over frameworks** – components interact through **feedback loops (events)**, not tight coupling.
* **Protocols first** – behavior is defined via `typing.Protocol`, not deep inheritance trees.
* **Replaceable infrastructure** – clocks, event engines, state stores, and runtimes can be swapped independently.
* **Explicit lifecycles** – devices and processes have clearly defined attach, boot, and shutdown phases.
* **Strict typing** – compatible with `mypy --strict` without sacrificing flexibility.

> If you’re looking for batteries-included automation, this is **not** it.
> If you want a clean core to build *your own* system, you’re in the right place.

---

## Core Concepts

### Runtime

The **Runtime** coordinates the system. Responsibilities include:

* Managing devices and processes
* Creating the shared `Context`
* Emitting system lifecycle events (`system.booting`, `system.booted`, etc.)

```python
from bussdcc import Runtime

rt = Runtime()
rt.boot()
```

After boot, the runtime exposes a **Context** to all attached devices and processes.

---

### Context

The **Context** is a lightweight capability container passed to devices and processes.

It provides:

* System clock access
* Event emission and subscription
* Runtime interface
* State access

```python
# Sleep for 1 second
ctx.sleep(1.0)

# Emit a custom event
ctx.emit("custom.event", value=42)

# Subscribe to all events
sub = ctx.on(lambda evt: print(evt.name, evt.data))

# Unsubscribe
sub.cancel()
```

> Note: `Context` **does not own policy** or decision-making logic — it only exposes capabilities.

---

### Devices

Devices represent **hardware, external resources, or boundary integrations**.

Device lifecycle:

* `attach(ctx)` → acquire resources
* `detach()` → release resources

```python
from bussdcc.device import Device

class Camera(Device):
    name = "camera"

    def connect(self):
        print("Camera online")

    def disconnect(self):
        print("Camera offline")
```

Devices automatically emit lifecycle events:

* `device.attached`
* `device.detached`
* `device.failed`

---

### Processes

Processes are **event-driven units of work**. They:

* Subscribe to events
* React to events in `on_event()`
* Support `on_start()` and `on_stop()` lifecycle hooks

```python
from bussdcc.process import Process

class Logger(Process):
    name = "logger"

    def on_event(self, ctx, evt):
        print(f"[{evt.time}] {evt.name}: {evt.data}")
```

Processes can be supervised and restarted by higher-level logic if desired.

Lifecycle events emitted by processes include:

* `process.started`
* `process.stopped`
* `process.error`

---

### Events

bussdcc uses a **synchronous, in-process event bus**.

* Events are named strings with keyword payloads.
* Callbacks are registered via `Context.on()`.
* Subscriptions can be cancelled at any time.

```python
sub = rt.ctx.on(lambda evt: print(evt.name, evt.data))
```

The event engine is **thread-safe, deterministic, and minimal**.

---

## What bussdcc Is (and Isn’t)

**It is:**

* A cybernetic kernel
* A coordination layer for IoT or automation
* A foundation for durable, event-driven systems

**It is not:**

* An application framework
* A scheduler or cron replacement
* An opinionated automation platform

You can build higher-level frameworks, supervisors, or schedulers *on top*.

---

## Status

**Pre-alpha.**
The core architecture is stabilizing, but APIs may still evolve.

---

## License

MIT License

---

> *Durable systems start with clear contracts, explicit lifecycles, and honest boundaries.*
