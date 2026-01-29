# BussDCC

**bussdcc** (Bussdieker Durable Cybernetic Core) is a minimal, strongly‑typed cybernetic runtime for Python.

It provides a small but resilient core for building systems that coordinate **devices**, **services**, and **processes** through explicit lifecycles and event‑driven communication.

The project is intentionally minimal: it defines *contracts and flow*, not policy.

---

## Design Philosophy

bussdcc is built around a few core ideas:

* **Cybernetics over frameworks** – components interact through feedback (events), not tight coupling.
* **Protocols first** – behavior is defined by contracts (`typing.Protocol`), not inheritance trees.
* **Replaceable infrastructure** – clocks, event buses, and runtimes can be swapped without refactors.
* **Explicit lifecycles** – devices and systems have clear attach/boot/shutdown phases.
* **Strict typing** – designed to pass `mypy --strict` without sacrificing flexibility.

If you’re looking for batteries‑included automation, this is not it.
If you want a clean core to build *your own* system on, you’re in the right place.

---

## Core Concepts

### Runtime

The `Runtime` is the system coordinator. It:

* Owns the system clock
* Manages registered devices
* Creates the shared `Context`
* Emits lifecycle events (`system.booting`, `system.booted`, etc.)

```python
from bussdcc import Runtime

rt = Runtime()
rt.boot()
```

---

### Context

The `Context` is a lightweight capability container passed to devices and services.

It provides access to:

* The system clock
* The runtime interface
* The event bus

```python
ctx.sleep(1.0)
ctx.emit("custom.event", value=42)
```

Context does **not** own policy or state — it only exposes capabilities.

---

### Devices

Devices represent hardware, external resources, or boundary integrations.

They follow a simple lifecycle:

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

### Events

bussdcc uses a simple event bus abstraction.

Events are:

* Named by string
* Emitted with keyword payloads
* Handled by registered callbacks

```python
rt.ctx.on("device.attached", lambda device: print("Attached:", device))
```

The default `EventBus` is synchronous and in‑process, but the interface allows other implementations.

---

## What bussdcc Is (and Isn’t)

**It is:**

* A cybernetic kernel
* A coordination layer
* A foundation for IoT, automation, and autonomous systems

**It is not:**

* An application framework
* A task scheduler
* An opinionated automation platform

Those can be built *on top*.

---

## Status

**Pre‑alpha.**

The core architecture is stabilizing, but APIs may still evolve.

---

## License

MIT License

---

> *Durable systems start with clear contracts and honest boundaries.*
