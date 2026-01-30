# BussDCC

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-brightgreen)

**bussdcc** (Bussdieker Durable Cybernetic Core) is a **minimal, strongly-typed cybernetic runtime for Python**.

It provides a resilient core for building systems that coordinate **devices**, **processes**, and **services** through **explicit lifecycles**, **event-driven communication**, and **strict typing**.

The project is intentionally **lightweight**: it defines *contracts and flow*, not application policies.

## Quick Start

```python
from bussdcc import Runtime
from bussdcc.device import Device
from bussdcc.process import Process
from bussdcc.service import Service

# Define components
class MyDevice(Device):
    name = "device1"
    def connect(self): print("Device online")
    def disconnect(self): print("Device offline")

class MyProcess(Process):
    name = "logger"
    def on_event(self, ctx, evt): print(evt.name, evt.data)

class MyService(Service):
    name = "heartbeat"
    interval = 2.0
    def tick(self, ctx): ctx.emit("heartbeat.tick")

# Create runtime and register components
rt = Runtime()
rt.register_device(MyDevice())
rt.register_process(MyProcess())
rt.register_service(MyService())

# Boot the system
rt.boot()
```

## Design Philosophy

bussdcc is built around a few guiding principles:

* **Cybernetics over frameworks** – components interact through **feedback loops (events)**, not tight coupling.
* **Protocols first** – behavior is defined via `typing.Protocol`, not deep inheritance trees.
* **Replaceable infrastructure** – clocks, event engines, state stores, and runtimes can be swapped independently.
* **Explicit lifecycles** – devices, processes, and services have clearly defined attach, boot, tick, and shutdown phases.
* **Strict typing** – compatible with `mypy --strict` without sacrificing flexibility.

> If you’re looking for batteries-included automation, this is **not** it.
> If you want a clean core to build *your own* system, you’re in the right place.

## Core Concepts

### Runtime

The **Runtime** coordinates the system: manages devices, processes, and services, creates the shared `Context`, and emits system lifecycle events (`system.booting`, `system.booted`, etc.).

### Context

A lightweight capability container: system clock, event emission/subscription, runtime interface, and state access.

### Devices

Represent **hardware, external resources, or boundary integrations**. Lifecycle: `attach(ctx)` → `detach()`. Emit: `device.attached`, `device.detached`, `device.failed`.

### Processes

Event-driven units of work. Lifecycle hooks: `on_start(ctx)`, `on_stop(ctx)`, `on_event(ctx, evt)`. Emit: `process.started`, `process.stopped`, `process.error`.

### Services

Long-running components orchestrated by the **ServiceSupervisor**. Lifecycle: `start(ctx)`, `tick(ctx)`, `stop(ctx)`. Supervisor handles:

* Automatic restarts
* Critical failure handling
* Threaded execution

Events: `service.started`, `service.stopped`, `service.error`, `service.restart`, `service.critical_failure`.

### Events

Synchronous, in-process, thread-safe event bus. Subscriptions can be cancelled. Events: named strings with keyword payloads.

## What bussdcc Is (and Isn’t)

**It is:**

* A cybernetic kernel
* A coordination layer for IoT or automation
* A foundation for durable, event-driven systems

**It is not:**

* An application framework
* A scheduler or cron replacement
* An opinionated automation platform

## Status

**Pre-alpha.** APIs may still evolve.

## License

MIT License

> *Durable systems start with clear contracts, explicit lifecycles, and honest boundaries.*

## Links

* [Repository](https://github.com/jbussdieker/bussdcc)
* [Issues](https://github.com/jbussdieker/bussdcc/issues)
* [Documentation](https://github.com/jbussdieker/bussdcc/blob/main/README.md)
