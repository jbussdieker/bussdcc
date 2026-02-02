# BussDCC

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-brightgreen)

**bussdcc** (Bussdieker Durable Cybernetic Core) is a **minimal, strongly-typed cybernetic runtime for Python**.

It provides a resilient core for building systems that coordinate **devices**, **processes**, **services**, and **interfaces** through **explicit lifecycles**, **event-driven communication**, and **strict typing**.

The project is intentionally **lightweight**: it defines *contracts and flow*, not application policy.

## Quick Start

```python
from bussdcc import Runtime
from bussdcc.device import Device
from bussdcc.process import Process
from bussdcc.service import Service

class MyDevice(Device):
    name = "device1"
    def connect(self): print("Device online")
    def disconnect(self): print("Device offline")

class MyProcess(Process):
    name = "logger"
    def on_event(self, ctx, evt):
        print(evt.name, evt.data)

class MyService(Service):
    name = "heartbeat"
    interval = 2.0
    def tick(self, ctx):
        ctx.events.emit("heartbeat.tick")

rt = Runtime()
rt.register_device(MyDevice())
rt.register_process(MyProcess())
rt.register_service(MyService())
rt.boot()
```

## Design Philosophy

bussdcc is built around a few guiding principles:

* **Cybernetics over frameworks** — systems coordinate through *feedback loops (events)*, not tight coupling.
* **Protocols first** — behavior is defined via `typing.Protocol`, not deep inheritance.
* **Replaceable infrastructure** — clocks, event engines, state stores, and runtimes are swappable.
* **Explicit lifecycles** — startup, attachment, execution, and shutdown are visible and ordered.
* **Strict typing** — compatible with `mypy --strict` without sacrificing flexibility.

> This is not an automation framework.
> It is a **kernel** for building your own.

## Core Concepts

### Runtime

The **Runtime** coordinates the system:

* Manages devices, processes, services, and interfaces
* Constructs the shared `Context`
* Emits lifecycle events:

  * `system.booting`
  * `system.booted`
  * `system.shutting_down`
  * `system.shutdown`

Boot order is **deterministic**:

1. Devices attach
2. Processes attach
3. Interfaces attach
4. Services start (under supervision)

Shutdown reverses this order.

### Context

A lightweight capability container shared by all components.

Provides access to:

* `clock` — monotonic + UTC time
* `events` — synchronous event bus
* `state` — thread-safe hierarchical state
* `runtime` — runtime introspection and lookup

The context is **intentionally small** and **side-effect free**.

### Clock

Clocks are abstracted via a protocol.

Default: `SystemClock`, providing:

* `now_utc()`
* `monotonic()`
* `uptime()`
* `sleep(seconds)`

Custom clocks (simulated, deterministic, test clocks) can be injected into the runtime.

### Events

Synchronous, in-process, thread-safe event engine.

* Events are named strings with structured payloads
* Handlers run **in the emitter’s thread**
* Subscriber failures are isolated and reported as `event.subscriber_error`
* Subscriptions are cancellable

This is **coordination**, not messaging middleware.

### State

Thread-safe hierarchical state engine with dot-path access:

```python
ctx.state.set("system.clock.uptime", 42)
ctx.state.get("system.clock.uptime")
```

* No schema enforcement
* No persistence (by design)
* Intended for coordination and observation, not storage

### Devices

Devices represent **hardware, external resources, or system boundaries**.

Lifecycle:

```
attach(ctx) → connect()
detach()   → disconnect()
```

Events emitted:

* `device.attached`
* `device.detached`
* `device.failed`

Devices are expected to be **honest about failure**.

### Processes

Processes are **event-driven units of work**.

They:

* Subscribe to the event engine
* React synchronously to events
* May emit new events or update state

Lifecycle hooks:

* `attach(ctx)`
* `on_start(ctx)`
* `on_event(ctx, evt)`
* `on_stop(ctx)`
* `detach()`

Errors are isolated and reported as `process.error`.

### Interfaces

Interfaces are **processes by role**, not by mechanism.

They typically:

* Translate human, network, or UI inputs into events
* Present system state outward
* Remain event-driven like any other process

They attach and detach alongside processes but are registered separately for clarity.

### Services

Services are **long-running, time-driven components**, managed by the `ServiceSupervisor`.

Characteristics:

* Run in their own threads
* Execute `tick(ctx)` on an interval
* Can restart automatically on failure
* May be marked `critical`

Lifecycle:

* `start(ctx)`
* `tick(ctx)` (loop)
* `stop(ctx)`

Supervisor events:

* `service.started`
* `service.stopped`
* `service.error`
* `service.restart`
* `service.critical_failure`

### Policies

Policies answer a single question:

> **“Should this happen?”**

They are **pure evaluators**, not controllers.

```python
class MyPolicy:
    name = "office_hours"

    def evaluate(self, ctx, evt=None) -> bool:
        hour = ctx.clock.now_utc().hour
        return 9 <= hour < 17
```

Key properties:

* No lifecycle
* No side effects
* No authority
* Callable by any component

Policies are **consulted**, never enforced by the runtime.

## What bussdcc Is (and Isn’t)

**It is:**

* A cybernetic coordination kernel
* A foundation for durable, event-driven systems
* Suitable for IoT, automation, robotics, and control planes

**It is not:**

* An application framework
* A scheduler or cron replacement
* A rules engine or policy engine
* Batteries included

## Status

**Pre-alpha.**
APIs may evolve, but core concepts are stabilizing.

## License

MIT License

> *Durable systems start with clear contracts, explicit lifecycles, and honest boundaries.*

## Links

* Repository: [https://github.com/jbussdieker/bussdcc](https://github.com/jbussdieker/bussdcc)
* Issues: [https://github.com/jbussdieker/bussdcc/issues](https://github.com/jbussdieker/bussdcc/issues)
* Changelog: [https://github.com/jbussdieker/bussdcc/blob/main/CHANGELOG.md](https://github.com/jbussdieker/bussdcc/blob/main/CHANGELOG.md)
